from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import datetime, timedelta

from models import User, Auction, AuctionBid, Notification, AutoBid

auction = Blueprint('auction', __name__)


# -----------------------------
# Get All Active Auctions
# -----------------------------
@auction.route('/auctions', methods=['GET'])
def get_auctions():
    """Get all active auctions"""
    category = request.args.get('category', 'all')
    
    # Check and end expired auctions
    now = datetime.utcnow()
    expired = Auction.objects(end_time__lt=now, is_ended=False)
    for a in expired:
        end_auction(a)
    
    # Check expired payments (45-min deadline passed)
    check_expired_payments()
    
    # Query auctions
    if category == 'all':
        auctions = Auction.objects(is_active=True, is_ended=False).order_by('-created_at')
    else:
        auctions = Auction.objects(is_active=True, is_ended=False, category=category).order_by('-created_at')
    
    result = []
    for a in auctions:
        time_left = (a.end_time - now).total_seconds() if a.end_time > now else 0
        result.append({
            "id": str(a.id),
            "title": a.title,
            "description": a.description,
            "image_url": a.image_url,
            "category": a.category,
            "starting_price": float(a.starting_price),
            "current_price": float(a.current_price),
            "min_bid_increment": float(a.min_bid_increment),
            "total_bids": a.total_bids,
            "time_left": int(time_left),
            "end_time": a.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            "seller": {
                "id": str(a.seller.id),
                "username": a.seller.username,
                "shop_name": a.seller.shop_name
            }
        })
    
    return jsonify({"auctions": result}), 200


# -----------------------------
# Get Single Auction
# -----------------------------
@auction.route('/auctions/<auction_id>', methods=['GET'])
def get_auction(auction_id):
    """Get auction details with full bid history"""
    try:
        a = Auction.objects.get(id=ObjectId(auction_id))
    except:
        return jsonify({"msg": "Auction not found"}), 404
    
    now = datetime.utcnow()
    time_left = (a.end_time - now).total_seconds() if a.end_time > now else 0
    
    # Get ALL bids for this auction (not just 20)
    bids = AuctionBid.objects(auction=a).order_by('-created_at')
    bid_history = []
    for idx, b in enumerate(bids):
        bid_history.append({
            "id": str(b.id),
            "rank": idx + 1,  # อันดับ (1 = ล่าสุด/สูงสุด)
            "bidder_id": str(b.bidder.id),
            "bidder_username": b.bidder.username,
            "bidder_avatar": b.bidder.profile_image_url if hasattr(b.bidder, 'profile_image_url') else None,
            "amount": float(b.amount),
            "time": b.created_at.strftime("%H:%M:%S"),
            "date": b.created_at.strftime("%d/%m/%Y"),
            "datetime": b.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "is_highest": idx == 0  # เสนอราคาสูงสุดหรือไม่
        })
    
    # นับจำนวน unique bidders
    unique_bidders = len(set([b.bidder_id for b in bid_history]))
    
    return jsonify({
        "id": str(a.id),
        "title": a.title,
        "description": a.description,
        "image_url": a.image_url,
        "category": a.category,
        "starting_price": float(a.starting_price),
        "current_price": float(a.current_price),
        "min_bid_increment": float(a.min_bid_increment),
        "total_bids": a.total_bids,
        "unique_bidders": unique_bidders,
        "time_left": int(time_left),
        "start_time": a.start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": a.end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "is_ended": a.is_ended,
        "winner": {
            "id": str(a.winner.id),
            "username": a.winner.username
        } if a.winner else None,
        "seller": {
            "id": str(a.seller.id),
            "username": a.seller.username,
            "shop_name": a.seller.shop_name
        },
        "bid_history": bid_history
    }), 200


# -----------------------------
# Place a Bid (Using Tokens)
# -----------------------------
@auction.route('/auctions/<auction_id>/bid', methods=['POST'])
@jwt_required()
def place_bid(auction_id):
    """Place a bid on an auction using tokens"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    try:
        a = Auction.objects.get(id=ObjectId(auction_id))
    except:
        return jsonify({"msg": "Auction not found"}), 404
    
    # Check if auction is active
    now = datetime.utcnow()
    if a.end_time <= now or a.is_ended:
        return jsonify({"msg": "การประมูลสิ้นสุดแล้ว"}), 400
    
    if str(a.seller.id) == user_id:
        return jsonify({"msg": "ไม่สามารถประมูลสินค้าของตัวเองได้"}), 400
    
    data = request.get_json()
    bid_amount = int(data.get('amount', 0))  # Token เป็น integer
    
    min_bid = int(a.current_price) + int(a.min_bid_increment)
    if bid_amount < min_bid:
        return jsonify({"msg": f"Token ต้องไม่น้อยกว่า {min_bid:,} Token"}), 400
    
    # ตรวจสอบ Token balance
    user_token_balance = user.token_balance or 0
    if user_token_balance < bid_amount:
        return jsonify({
            "msg": f"Token ไม่เพียงพอ คุณมี {user_token_balance:,} Token แต่ต้องการ {bid_amount:,} Token",
            "token_balance": user_token_balance,
            "required": bid_amount
        }), 400
    
    # หา previous highest bidder เพื่อคืน Token
    previous_highest_bid = AuctionBid.objects(auction=a).order_by('-amount').first()
    previous_bidder = previous_highest_bid.bidder if previous_highest_bid else None
    previous_amount = int(previous_highest_bid.amount) if previous_highest_bid else 0
    
    # หัก Token จาก user ที่ประมูล
    user.token_balance = user_token_balance - bid_amount
    user.save()
    
    # คืน Token ให้คนที่ถูกแซง (ถ้ามี และไม่ใช่คนเดียวกัน)
    if previous_bidder and str(previous_bidder.id) != user_id:
        previous_bidder.token_balance = (previous_bidder.token_balance or 0) + previous_amount
        previous_bidder.save()
        
        # แจ้งเตือนคนที่ถูกแซง
        Notification(
            user=previous_bidder,
            title="⚠️ มีคนเสนอราคาสูงกว่า!",
            message=f"คุณถูกแซงในการประมูล '{a.title}' และได้รับ {previous_amount:,} Token คืนแล้ว",
            type="order",
            link=f"/auction"
        ).save()
    
    # Create bid
    new_bid = AuctionBid(
        auction=a,
        bidder=user,
        amount=bid_amount
    )
    new_bid.save()
    
    # Update auction
    a.current_price = bid_amount
    a.total_bids += 1
    a.winner = user  # Tentative winner
    a.save()
    
    return jsonify({
        "msg": "ประมูลสำเร็จ!",
        "current_price": int(a.current_price),
        "total_bids": a.total_bids,
        "your_bid": bid_amount,
        "remaining_tokens": user.token_balance
    }), 200


# -----------------------------
# Constants & Helpers for Upload
# -----------------------------
import os
import uuid

UPLOAD_FOLDER = 'uploads/products'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(image_file):
    if image_file and allowed_file(image_file.filename):
        ext = image_file.filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{ext}"
        file_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        image_file.save(file_path)
        return f"/uploads/products/{unique_filename}"
    return None


# -----------------------------
# Create Auction (Seller)
# -----------------------------
@auction.route('/auctions', methods=['POST'])
@jwt_required()
def create_auction():
    """Create a new auction"""
    try:
        user_id = get_jwt_identity()
        user = User.objects(id=ObjectId(user_id)).first()
        
        if not user or not user.is_seller:
            return jsonify({"msg": "เฉพาะผู้ขายเท่านั้นที่สามารถสร้างการประมูลได้"}), 403
        
        # Handle form-data (Multipart)
        data = request.form
        
        title = data.get('title')
        description = data.get('description', '')
        image_url = data.get('image_url')
        category = data.get('category', 'all')
        starting_price = float(data.get('starting_price', 0))
        duration_minutes = int(data.get('duration_minutes', 0))
        try:
            duration_hours = float(data.get('duration_hours', 24))
        except ValueError:
            duration_hours = 24
            
        min_bid_increment = float(data.get('min_bid_increment', 10))
        
        # Handle Image Upload if provided
        if 'image' in request.files:
            file = request.files['image']
            if file.filename != '':
                uploaded_url = save_image(file)
                if uploaded_url:
                    image_url = uploaded_url

        if not title or starting_price <= 0:
            return jsonify({"msg": "ต้องระบุชื่อและราคาเริ่มต้น"}), 400
        
        # Calculate end time
        if duration_minutes > 0:
            end_time = datetime.utcnow() + timedelta(minutes=duration_minutes)
        else:
            end_time = datetime.utcnow() + timedelta(hours=duration_hours)
        
        new_auction = Auction(
            title=title,
            description=description,
            image_url=image_url,
            category=category,
            starting_price=starting_price,
            current_price=starting_price,
            min_bid_increment=min_bid_increment,
            seller=user,
            end_time=end_time
        )
        new_auction.save()
        
        return jsonify({
            "msg": "สร้างการประมูลสำเร็จ!",
            "auction_id": str(new_auction.id),
            "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S")
        }), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"msg": f"Internal Server Error: {str(e)}"}), 500


# -----------------------------
# Helper: End Auction
# -----------------------------
def end_auction(auction):
    """End an auction, set payment deadline, and send invoice via chat"""
    from models import Conversation, Message
    
    auction.is_ended = True
    auction.is_active = False
    
    if auction.winner:
        # Set 45-minute payment deadline
        auction.payment_deadline = datetime.utcnow() + timedelta(minutes=45)
        auction.payment_status = 'pending'
        
        # Create or get conversation between winner and seller for invoice
        existing_conv = Conversation.objects(
            participants__all=[auction.winner, auction.seller]
        ).first()
        
        if existing_conv:
            conv = existing_conv
        else:
            conv = Conversation(
                participants=[auction.winner, auction.seller]
            )
            conv.save()
        
        auction.invoice_conversation_id = str(conv.id)
        
        # Create invoice message
        deadline_str = (auction.payment_deadline + timedelta(hours=7)).strftime("%H:%M น.")  # Convert to Thai time
        invoice_message = f"""🧾 **ใบแจ้งชำระเงิน - การประมูล**

📦 สินค้า: {auction.title}
💰 ราคาชนะ: {int(auction.current_price):,} Token

⏰ กรุณาชำระภายใน: **{deadline_str}** (45 นาที)

หากไม่ชำระภายในเวลาที่กำหนด การประมูลจะถูกยกเลิกและ Token จะถูกคืนให้ผู้ประมูลคนก่อนหน้า

กดปุ่ม "ชำระเงิน" ในหน้ารายละเอียดการประมูลเพื่อยืนยันการชำระ
/auction/{str(auction.id)}"""
        
        Message(
            conversation=conv,
            sender=auction.seller,
            content=invoice_message
        ).save()
        
        # Update conversation last message
        conv.last_message = "🧾 ใบแจ้งชำระเงิน - การประมูล"
        conv.last_message_at = datetime.utcnow()
        conv.save()
        
        # Notify winner
        Notification(
            user=auction.winner,
            title="🎉 คุณชนะการประมูล!",
            message=f"คุณชนะ '{auction.title}' ในราคา {int(auction.current_price):,} Token - กรุณาชำระภายใน 45 นาที",
            type="order",
            link=f"/chat?conversationId={str(conv.id)}"
        ).save()
        
        # Notify seller
        Notification(
            user=auction.seller,
            title="🔨 การประมูลสิ้นสุด",
            message=f"'{auction.title}' ขายได้ในราคา {int(auction.current_price):,} Token",
            type="order",
            link=f"/chat?conversationId={str(conv.id)}"
        ).save()
    
    auction.save()


# -----------------------------
# Pay for Won Auction
# -----------------------------
@auction.route('/auctions/<auction_id>/pay', methods=['POST'])
@jwt_required()
def pay_auction(auction_id):
    """Winner pays for the auction using tokens (already held)"""
    from models import Conversation, Message, WalletHistory
    
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    try:
        a = Auction.objects.get(id=ObjectId(auction_id))
    except:
        return jsonify({"msg": "Auction not found"}), 404
    
    # Verify this is the winner
    if not a.winner or str(a.winner.id) != user_id:
        return jsonify({"msg": "คุณไม่ใช่ผู้ชนะการประมูลนี้"}), 403
    
    # Check if already paid
    if a.payment_status == 'paid':
        return jsonify({"msg": "ชำระเงินแล้ว"}), 400
    
    # Check if expired
    if a.payment_status == 'expired':
        return jsonify({"msg": "หมดเวลาชำระเงินแล้ว"}), 400
    
    # Check deadline
    if a.payment_deadline and datetime.utcnow() > a.payment_deadline:
        a.payment_status = 'expired'
        a.save()
        return jsonify({"msg": "หมดเวลาชำระเงินแล้ว (เกิน 45 นาที)"}), 400
    
    # Token is already held from bidding, now transfer to seller
    amount = int(a.current_price)
    seller = a.seller
    
    seller_balance_before = seller.token_balance or 0
    seller.token_balance = seller_balance_before + amount
    seller.total_sales = (seller.total_sales or 0) + amount
    seller.save()
    
    # Record transaction for seller
    WalletHistory(
        user=seller,
        type='income',
        amount=amount,
        balance_before=seller_balance_before,
        balance_after=seller.token_balance,
        description=f"Auction Sale: {a.title[:30]}",
        reference_id=str(a.id)
    ).save()
    
    # Update auction status
    a.payment_status = 'paid'
    a.is_active = False  # ✅ Remove from auction list
    a.save()
    
    # ✅ Create Order for purchase history
    from models import Order
    new_order = Order(
        user=user,
        items=[],  # Auction items don't have CartItem, so empty
        total_price=amount,
        status='processing',  # เริ่มด้วยสถานะกำลังจัดส่งเลย เพราะ Token ถูกหักตอนประมูลแล้ว
        created_at=datetime.utcnow()
    )
    new_order.save()
    
    # Record buyer transaction in WalletHistory (already deducted during bidding)
    WalletHistory(
        user=user,
        type='payment',
        amount=-amount,
        balance_before=user.token_balance + amount,  # Approximate (was deducted during bid)
        balance_after=user.token_balance,
        description=f"Auction Purchase: {a.title[:30]}",
        reference_id=str(new_order.id)
    ).save()
    
    # Send confirmation message in chat
    if a.invoice_conversation_id:
        try:
            conv = Conversation.objects.get(id=ObjectId(a.invoice_conversation_id))
            Message(
                conversation=conv,
                sender=user,
                content=f"✅ ชำระเงินสำเร็จ! {amount:,} Token ถูกโอนให้ผู้ขายแล้ว"
            ).save()
            conv.last_message = "✅ ชำระเงินสำเร็จ!"
            conv.last_message_at = datetime.utcnow()
            conv.save()
        except:
            pass
    
    # Notify seller
    Notification(
        user=seller,
        title="💰 ได้รับเงินจากการประมูล",
        message=f"คุณได้รับ {amount:,} Token จากการขาย '{a.title}'",
        type="order",
        link="/seller-dashboard"
    ).save()
    
    return jsonify({
        "msg": "ชำระเงินสำเร็จ!",
        "amount": amount,
        "auction_title": a.title,
        "order_id": str(new_order.id)
    }), 200


# -----------------------------
# Check and Handle Expired Auctions
# -----------------------------
def check_expired_payments():
    """Check for auctions past payment deadline and handle them"""
    now = datetime.utcnow()
    
    # Find auctions that are ended, pending payment, and past deadline
    expired = Auction.objects(
        is_ended=True,
        payment_status='pending',
        payment_deadline__lt=now
    )
    
    for a in expired:
        a.payment_status = 'expired'
        
        # Return token to the winner (optional: could give to next bidder)
        if a.winner:
            amount = int(a.current_price)
            a.winner.token_balance = (a.winner.token_balance or 0) + amount
            a.winner.save()
            
            # Notify winner about expiry
            Notification(
                user=a.winner,
                title="⚠️ การชำระเงินหมดเวลา",
                message=f"คุณไม่ได้ชำระเงินสำหรับ '{a.title}' ภายใน 45 นาที - Token {amount:,} ถูกคืนให้แล้ว",
                type="order"
            ).save()
            
            # Notify seller
            Notification(
                user=a.seller,
                title="❌ การประมูลถูกยกเลิก",
                message=f"ผู้ชนะไม่ชำระเงินสำหรับ '{a.title}' ภายในเวลาที่กำหนด",
                type="order"
            ).save()
        
        a.save()


# -----------------------------
# Seed Demo Auctions
# -----------------------------
@auction.route('/auctions/seed', methods=['POST'])
def seed_auctions():
    """Create demo auctions"""
    # Get demo seller
    demo_seller = User.objects(username="P2UKAISER_Shop").first()
    if not demo_seller:
        return jsonify({"msg": "Demo seller not found"}), 404
    
    # Clear existing
    Auction.objects.delete()
    AuctionBid.objects.delete()
    
    demo_auctions = [
        {
            "title": "iPhone 15 Pro Max Limited Edition",
            "description": "iPhone 15 Pro Max สี Natural Titanium สภาพใหม่ 99% ประกันเหลือ 10 เดือน",
            "image_url": "/static/products/product_iphone_1766769641862.png",
            "category": "electronics",
            "starting_price": 25000,
            "duration_hours": 48
        },
        {
            "title": "PlayStation 5 Bundle พร้อมเกม",
            "description": "PS5 + DualSense 2 ตัว + เกม 5 แผ่น สภาพเยี่ยม",
            "image_url": "/static/products/product_ps5_1766770153698.png",
            "category": "gaming",
            "starting_price": 12000,
            "duration_hours": 24
        },
        {
            "title": "MacBook Pro M2 14 นิ้ว",
            "description": "MacBook Pro 14 M2 Pro RAM 16GB SSD 512GB ใช้งานได้ปกติ",
            "image_url": "/static/products/product_macbook_1766770139240.png",
            "category": "electronics",
            "starting_price": 35000,
            "duration_hours": 72
        },
        {
            "title": "Air Jordan 1 Retro High OG",
            "description": "รองเท้า Jordan 1 ของแท้ Size 42 สภาพ 9/10",
            "image_url": "/static/products/product_sneakers_1766769676542.png",
            "category": "fashion",
            "starting_price": 5000,
            "duration_hours": 12
        },
        {
            "title": "Apple Watch Ultra Titanium",
            "description": "Apple Watch Ultra ตัวท็อป GPS+Cellular สภาพใหม่มาก",
            "image_url": "/static/products/product_watch_1766769694809.png",
            "category": "electronics",
            "starting_price": 18000,
            "duration_hours": 36
        },
    ]
    
    created = []
    for a in demo_auctions:
        end_time = datetime.utcnow() + timedelta(hours=a['duration_hours'])
        new_auction = Auction(
            title=a['title'],
            description=a['description'],
            image_url=a['image_url'],
            category=a['category'],
            starting_price=a['starting_price'],
            current_price=a['starting_price'],
            min_bid_increment=100,
            seller=demo_seller,
            end_time=end_time
        )
        new_auction.save()
        created.append(a['title'])
    
    return jsonify({
        "msg": f"Created {len(created)} demo auctions",
        "auctions": created
    }), 201


# -----------------------------
# Auto-Bid: Set Auto Bid
# -----------------------------
@auction.route('/auctions/<auction_id>/auto-bid', methods=['POST'])
@jwt_required()
def set_auto_bid(auction_id):
    """Set auto-bid for an auction"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    if not user:
        return jsonify({"msg": "User not found"}), 404
    
    try:
        a = Auction.objects.get(id=ObjectId(auction_id))
    except:
        return jsonify({"msg": "Auction not found"}), 404
    
    if a.is_ended or datetime.utcnow() >= a.end_time:
        return jsonify({"msg": "การประมูลสิ้นสุดแล้ว"}), 400
    
    if str(a.seller.id) == user_id:
        return jsonify({"msg": "ไม่สามารถประมูลสินค้าของตัวเองได้"}), 400
    
    data = request.get_json()
    max_amount = float(data.get('max_amount', 0))
    
    min_bid = float(a.current_price) + float(a.min_bid_increment)
    if max_amount < min_bid:
        return jsonify({"msg": f"ราคาสูงสุดต้องไม่น้อยกว่า ฿{min_bid:,.0f}"}), 400
    
    # Check existing auto-bid
    existing = AutoBid.objects(auction=a, user=user, is_active=True).first()
    if existing:
        existing.max_amount = max_amount
        existing.save()
        msg = "อัปเดต Auto-Bid สำเร็จ"
    else:
        AutoBid(
            auction=a,
            user=user,
            max_amount=max_amount
        ).save()
        msg = "ตั้งค่า Auto-Bid สำเร็จ"
    
    # Process auto-bid immediately
    process_auto_bids(a)
    
    return jsonify({
        "msg": msg,
        "max_amount": max_amount,
        "current_price": float(a.current_price)
    }), 200


# -----------------------------
# Auto-Bid: Cancel Auto Bid
# -----------------------------
@auction.route('/auctions/<auction_id>/auto-bid', methods=['DELETE'])
@jwt_required()
def cancel_auto_bid(auction_id):
    """Cancel auto-bid for an auction"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    try:
        a = Auction.objects.get(id=ObjectId(auction_id))
    except:
        return jsonify({"msg": "Auction not found"}), 404
    
    auto_bid = AutoBid.objects(auction=a, user=user, is_active=True).first()
    if not auto_bid:
        return jsonify({"msg": "ไม่พบ Auto-Bid"}), 404
    
    auto_bid.is_active = False
    auto_bid.save()
    
    return jsonify({"msg": "ยกเลิก Auto-Bid สำเร็จ"}), 200


# -----------------------------
# Auto-Bid: Get My Auto Bids
# -----------------------------
@auction.route('/auctions/my-auto-bids', methods=['GET'])
@jwt_required()
def get_my_auto_bids():
    """Get all active auto-bids for current user"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    auto_bids = AutoBid.objects(user=user, is_active=True)
    
    result = []
    for ab in auto_bids:
        a = ab.auction
        if a.is_ended:
            continue
        
        result.append({
            "id": str(ab.id),
            "auction_id": str(a.id),
            "auction_title": a.title,
            "auction_image": a.image_url,
            "max_amount": float(ab.max_amount),
            "current_bid": float(ab.current_bid),
            "current_price": float(a.current_price),
            "is_winning": str(a.winner.id) == user_id if a.winner else False,
            "time_left": max(0, int((a.end_time - datetime.utcnow()).total_seconds()))
        })
    
    return jsonify({"auto_bids": result}), 200


# -----------------------------
# Auction History
# -----------------------------
@auction.route('/auctions/my-history', methods=['GET'])
@jwt_required()
def get_my_auction_history():
    """Get user's auction participation history"""
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()
    
    # Get unique auctions user has bid on
    user_bids = AuctionBid.objects(bidder=user).order_by('-created_at')
    auction_ids = list(set([str(b.auction.id) for b in user_bids]))
    
    result = {
        "won": [],
        "lost": [],
        "active": []
    }
    
    for aid in auction_ids:
        try:
            a = Auction.objects.get(id=ObjectId(aid))
        except:
            continue
        
        # Get user's highest bid
        user_highest = AuctionBid.objects(auction=a, bidder=user).order_by('-amount').first()
        
        auction_data = {
            "id": str(a.id),
            "title": a.title,
            "image_url": a.image_url,
            "current_price": float(a.current_price),
            "my_highest_bid": float(user_highest.amount) if user_highest else 0,
            "total_bids": a.total_bids,
            "end_time": a.end_time.isoformat(),
            "is_ended": a.is_ended
        }
        
        if a.is_ended:
            if a.winner and str(a.winner.id) == user_id:
                result["won"].append(auction_data)
            else:
                result["lost"].append(auction_data)
        else:
            auction_data["time_left"] = max(0, int((a.end_time - datetime.utcnow()).total_seconds()))
            auction_data["is_winning"] = str(a.winner.id) == user_id if a.winner else False
            result["active"].append(auction_data)
    
    return jsonify({
        "history": result,
        "stats": {
            "total_participated": len(auction_ids),
            "won": len(result["won"]),
            "lost": len(result["lost"]),
            "active": len(result["active"])
        }
    }), 200


# -----------------------------
# Helper: Process Auto-Bids
# -----------------------------
def process_auto_bids(auction):
    """Process all auto-bids for an auction"""
    if auction.is_ended:
        return
    
    # Get all active auto-bids, sorted by max_amount (highest first)
    auto_bids = AutoBid.objects(auction=auction, is_active=True).order_by('-max_amount')
    
    if len(auto_bids) < 1:
        return
    
    current_price = float(auction.current_price)
    increment = float(auction.min_bid_increment)
    
    # If only one auto-bidder, bid minimum
    if len(auto_bids) == 1:
        ab = auto_bids[0]
        if float(ab.max_amount) > current_price:
            new_price = current_price + increment
            if new_price <= float(ab.max_amount):
                place_auto_bid(auction, ab.user, new_price)
                ab.current_bid = new_price
                ab.save()
        return
    
    # Multiple auto-bidders: compete
    highest = auto_bids[0]
    second = auto_bids[1]
    
    # New price beats second highest by one increment
    new_price = min(float(highest.max_amount), float(second.max_amount) + increment)
    
    if new_price > current_price:
        place_auto_bid(auction, highest.user, new_price)
        highest.current_bid = new_price
        highest.save()


def place_auto_bid(auction, user, amount):
    """Place an auto-bid"""
    new_bid = AuctionBid(
        auction=auction,
        bidder=user,
        amount=amount
    )
    new_bid.save()
    
    # Update auction
    old_winner = auction.winner
    auction.current_price = amount
    auction.total_bids += 1
    auction.winner = user
    auction.save()
    
    # Notify previous winner if different
    if old_winner and str(old_winner.id) != str(user.id):
        Notification(
            user=old_winner,
            title="⚠️ Auto-Bid: มีคนเสนอราคาสูงกว่า!",
            message=f"มีคนเสนอราคา ฿{amount:,.0f} สำหรับ '{auction.title}'",
            type="order",
            link=f"/auctions/{str(auction.id)}"
        ).save()

