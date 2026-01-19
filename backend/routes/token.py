from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime

from models import User, TokenRequest, Notification, WalletHistory

token_bp = Blueprint('token', __name__)


# -----------------------------
# สร้างคำขอเติม Token
# -----------------------------
@token_bp.route('/token/request', methods=['POST'])
@jwt_required()
def create_token_request():
    """User creates a token top-up request"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    data = request.get_json()
    amount = data.get('amount')
    payment_proof_url = data.get('payment_proof_url', '')
    
    if not amount or amount <= 0:
        return jsonify({"msg": "กรุณาระบุจำนวน Token ที่ถูกต้อง"}), 400
    
    # สร้างคำขอ
    token_request = TokenRequest(
        user=user,
        amount=amount,
        payment_proof_url=payment_proof_url
    )
    token_request.save()
    
    return jsonify({
        "msg": "ส่งคำขอเติม Token สำเร็จ รอการอนุมัติจาก Admin",
        "request_id": str(token_request.id),
        "amount": amount,
        "status": "pending"
    }), 201


# -----------------------------
# ดูประวัติคำขอ Token ของตัวเอง
# -----------------------------
@token_bp.route('/token/my-requests', methods=['GET'])
@jwt_required()
def get_my_token_requests():
    """Get user's token request history"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    requests = TokenRequest.objects(user=user).order_by('-created_at')
    
    result = []
    for r in requests:
        result.append({
            "id": str(r.id),
            "amount": r.amount,
            "status": r.status,
            "payment_proof_url": r.payment_proof_url,
            "admin_note": r.admin_note,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "processed_at": r.processed_at.strftime("%Y-%m-%d %H:%M:%S") if r.processed_at else None
        })
    
    return jsonify({"requests": result}), 200


# -----------------------------
# ดูยอด Token คงเหลือ
# -----------------------------
@token_bp.route('/token/balance', methods=['GET'])
@jwt_required()
def get_token_balance():
    """Get user's token balance"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    return jsonify({
        "token_balance": user.token_balance or 0,
        "username": user.username
    }), 200


# -----------------------------
# ตรวจสอบสลิปและเติม Token อัตโนมัติ
# -----------------------------
@token_bp.route('/token/verify-slip', methods=['POST'])
@jwt_required()
def verify_slip_and_topup():
    """
    รับสลิปจากผู้ใช้ ตรวจสอบกับ SlipOK API
    ถ้าสลิปถูกต้อง จะเพิ่ม Token ให้อัตโนมัติตามยอดในสลิป
    """
    import json
    import os
    from werkzeug.utils import secure_filename
    from utils.slipok import verify_slip
    
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    # Check if file is uploaded
    if 'slip' not in request.files:
        return jsonify({"msg": "กรุณาอัปโหลดรูปสลิป"}), 400
    
    slip_file = request.files['slip']
    
    if slip_file.filename == '':
        return jsonify({"msg": "กรุณาเลือกไฟล์สลิป"}), 400
    
    # Check file extension
    allowed_extensions = {'png', 'jpg', 'jpeg', 'webp', 'jfif'}
    file_ext = slip_file.filename.rsplit('.', 1)[-1].lower()
    if file_ext not in allowed_extensions:
        return jsonify({"msg": "รองรับเฉพาะไฟล์รูปภาพ (PNG, JPG, JPEG, WEBP)"}), 400
    
    # Read file data
    slip_data = slip_file.read()
    
    # Save slip image
    upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'slips')
    os.makedirs(upload_folder, exist_ok=True)
    
    filename = f"{user_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{secure_filename(slip_file.filename)}"
    filepath = os.path.join(upload_folder, filename)
    
    with open(filepath, 'wb') as f:
        f.write(slip_data)
    
    slip_url = f"/uploads/slips/{filename}"
    
    # Verify slip with SlipOK API
    result = verify_slip(slip_data)
    
    if result['success']:
        # Slip is valid - get amount and create auto-approved request
        amount = int(result['amount'])
        
        if amount <= 0:
            return jsonify({
                "success": False,
                "msg": "ไม่พบยอดเงินในสลิป"
            }), 400
        
        # Check for duplicate transaction ref
        existing = TokenRequest.objects(transaction_ref=result['transaction_ref']).first()
        if existing:
            return jsonify({
                "success": False,
                "msg": "สลิปนี้เคยถูกใช้งานแล้ว",
                "error_code": 1012
            }), 400
        
        # Create auto-approved token request
        token_request = TokenRequest(
            user=user,
            amount=amount,
            payment_proof_url=slip_url,
            status='approved',
            admin_note='อนุมัติอัตโนมัติโดย SlipOK',
            slip_verify_data=json.dumps(result['data'], ensure_ascii=False),
            transaction_ref=result['transaction_ref'],
            verified_amount=amount,
            sender_name=result['sender']['name'],
            is_auto_approved=True,
            processed_at=datetime.utcnow()
        )
        token_request.save()
        
        # Add tokens to user
        user.token_balance = (user.token_balance or 0) + amount
        balance_before = user.token_balance or 0
        user.token_balance = balance_before + amount
        user.save()
        
        # 🔹 Record Transaction (Top-up)
        WalletHistory(
            user=user,
            type='topup',
            amount=amount,
            balance_before=balance_before,
            balance_after=user.token_balance,
            description="Auto Top-up via PromptPay",
            reference_id=result['transaction_ref']
        ).save()
        
        # Create notification
        Notification(
            user=user,
            title="✅ เติม Token สำเร็จ!",
            message=f"เพิ่ม {amount} Token จากการโอนเงินแล้ว ยอดคงเหลือ {user.token_balance} Token",
            type="system",
            link="/token-topup"
        ).save()
        
        return jsonify({
            "success": True,
            "msg": f"เติม Token สำเร็จ! ได้รับ {amount} Token",
            "amount": amount,
            "new_balance": user.token_balance,
            "transaction_ref": result['transaction_ref'],
            "sender_name": result['sender']['name']
        }), 200
        
    else:
        # Slip verification failed
        return jsonify({
            "success": False,
            "msg": result.get('error_message', 'ไม่สามารถตรวจสอบสลิปได้'),
            "error_code": result.get('error_code', 0)
        }), 400


# -----------------------------
# อัปโหลดสลิป (สำหรับ Manual Review)
# -----------------------------
@token_bp.route('/token/upload-slip', methods=['POST'])
@jwt_required()
def upload_slip_for_review():
    """
    อัปโหลดสลิปสำหรับให้ Admin ตรวจสอบแบบ Manual
    """
    import os
    from werkzeug.utils import secure_filename
    
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    if 'slip' not in request.files:
        return jsonify({"msg": "กรุณาอัปโหลดรูปสลิป"}), 400
    
    data = request.form
    amount = int(data.get('amount', 0))
    
    if amount <= 0:
        return jsonify({"msg": "กรุณาระบุจำนวน Token"}), 400
    
    slip_file = request.files['slip']
    
    if slip_file.filename == '':
        return jsonify({"msg": "กรุณาเลือกไฟล์สลิป"}), 400
    
    # Save slip image
    upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads', 'slips')
    os.makedirs(upload_folder, exist_ok=True)
    
    filename = f"{user_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{secure_filename(slip_file.filename)}"
    filepath = os.path.join(upload_folder, filename)
    slip_file.save(filepath)
    
    slip_url = f"/uploads/slips/{filename}"
    
    # Create pending token request
    token_request = TokenRequest(
        user=user,
        amount=amount,
        payment_proof_url=slip_url,
        status='pending'
    )
    token_request.save()
    
    return jsonify({
        "msg": "ส่งสลิปสำเร็จ รอ Admin ตรวจสอบ",
        "request_id": str(token_request.id),
        "amount": amount,
        "slip_url": slip_url
    }), 201


# -----------------------------
# Transaction History (Unified)
# -----------------------------
@token_bp.route('/wallet/history', methods=['GET'])
@jwt_required()
def get_wallet_history():
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    history = WalletHistory.objects(user=user).order_by('-created_at')
    
    result = []
    for h in history:
        result.append({
            "id": str(h.id),
            "type": h.type,
            "amount": h.amount,
            "balance_before": h.balance_before,
            "balance_after": h.balance_after,
            "description": h.description,
            "created_at": h.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return jsonify({"history": result}), 200

