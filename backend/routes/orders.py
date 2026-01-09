from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from mongoengine.errors import DoesNotExist
from datetime import datetime

from models import User, Order, CartItem, Product, Notification

orders = Blueprint('orders', __name__)

# -----------------------------
# 1. ดูประวัติการสั่งซื้อ (Order History)
# -----------------------------
@orders.route('/orders', methods=['GET'])
@jwt_required()
def get_order_history():
    user_id = get_jwt_identity()
    try:
        user = User.objects.get(id=ObjectId(user_id))
        user_orders = Order.objects(user=user).order_by('-created_at')
        
        result = []
        for order in user_orders:
            items_list = []
            for item_ref in order.items:
                try:
                    # ป้องกันกรณี item ถูกลบไปแล้วแต่ยังมี reference อยู่
                    if item_ref and item_ref.product:
                        items_list.append({
                            "product_id": str(item_ref.product.id),
                            "product_name": item_ref.product.name,
                            "product_image": item_ref.product.image_url,
                            "quantity": int(item_ref.quantity),
                            "price": float(item_ref.product.price)
                        })
                except: continue
            
            result.append({
                "id": str(order.id),
                "items": items_list,
                "total_price": float(order.total_price),
                "status": order.status,
                "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S") if order.created_at else "N/A"
            })
        
        return jsonify({"orders": result, "total": len(result)}), 200
    except DoesNotExist:
        return jsonify({"msg": "ไม่พบข้อมูลผู้ใช้"}), 404
    except Exception as e:
        return jsonify({"msg": f"เกิดข้อผิดพลาด: {str(e)}"}), 500

# -----------------------------
# 2. สร้างคำสั่งซื้อ (Checkout)
# -----------------------------
@orders.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    item_ids = data.get('cart_items', [])
    
    if not item_ids:
        return jsonify({"msg": "ไม่มีสินค้าที่เลือกชำระเงินเพคะ"}), 400
    
    try:
        user = User.objects.get(id=ObjectId(user_id))
        final_cart_items = []
        total_price = 0
        
        for item_id in item_ids:
            if not ObjectId.is_valid(item_id): continue
            oid = ObjectId(item_id)
            
            cart_item = CartItem.objects.filter(id=oid, user=user).first()
            if not cart_item:
                cart_item = CartItem.objects.filter(product=oid, user=user).first()
            
            if not cart_item:
                product = Product.objects.filter(id=oid).first()
                if product:
                    cart_item = CartItem(user=user, product=product, quantity=1)
                    cart_item.save()
            
            if cart_item and cart_item.product:
                final_cart_items.append(cart_item)
                total_price += float(cart_item.product.price) * int(cart_item.quantity)

        if not final_cart_items:
            return jsonify({"msg": "ไม่พบข้อมูลสินค้าที่ต้องการสั่งซื้อในระบบเพคะ"}), 400
        
        new_order = Order(
            user=user,
            items=final_cart_items,
            total_price=total_price,
            status='paid',
            created_at=datetime.utcnow()
        )
        new_order.save()
        
        # แจ้งเตือนผู้ขาย
        seller_notified = set()
        for item in final_cart_items:
            seller = item.product.seller
            if seller:
                seller_id_str = str(seller.id)
                if seller_id_str not in seller_notified:
                    Notification(
                        user=seller,
                        title="ยอดขายใหม่ ✨",
                        message=f"คุณได้รับออเดอร์ใหม่จากคุณ {user.username} แล้วเพคะ",
                        type="order",
                        link="/seller-dashboard"
                    ).save()
                    seller_notified.add(seller_id_str)
                
                # อัปเดตยอดขายสะสมของผู้ขาย
                current_sales = getattr(seller, 'total_sales', 0) or 0
                seller.total_sales = current_sales + (float(item.product.price) * int(item.quantity))
                seller.save()
        
        # ⚠️ สำคัญ: เราไม่ delete item ทิ้งทันที เพราะ Order ยังอ้างอิงอยู่ 
        # หรือควรเปลี่ยน Model Order ให้เก็บข้อมูลแบบ Snapshot (แต่ตอนนี้แก้ที่ตัวดึงข้อมูลก่อน)

        return jsonify({
            "msg": "สั่งซื้อสำเร็จแล้วเพคะ! ✨",
            "order_id": str(new_order.id),
            "total_price": total_price
        }), 201
    except Exception as e:
        print(f"Checkout Error: {str(e)}")
        return jsonify({"msg": f"เกิดข้อผิดพลาดที่ระบบ: {str(e)}"}), 500

# -----------------------------
# 4. ดูออเดอร์ของผู้ขาย (Seller Orders) - ปรับปรุงการตรวจสอบ
# -----------------------------
@orders.route('/orders/seller/<seller_id>', methods=['GET'])
@jwt_required()
def get_seller_orders(seller_id):
    user_id = get_jwt_identity()
    # ตรวจสอบว่าผู้เรียกเป็น Seller จริงหรือไม่
    current_user = User.objects(id=ObjectId(user_id), is_seller=True).first()
    
    if not current_user or str(current_user.id) != seller_id:
        return jsonify({"msg": "Unauthorized"}), 403

    try:
        seller_oid = ObjectId(seller_id)
        # ดึงออเดอร์ทั้งหมดมาฟิลเตอร์ (เนื่องจากโครงสร้าง items เป็น List of References)
        all_orders = Order.objects().order_by('-created_at')

        result = []
        for order in all_orders:
            seller_items = []
            for item in order.items:
                try:
                    # ตรวจสอบว่า item ยังอยู่ และ product ยังอยู่
                    if item and item.product:
                        # ตรวจสอบว่าเจ้าของสินค้าคือ seller_id ที่ส่งมาหรือไม่
                        product_seller = item.product.seller
                        if product_seller and str(product_seller.id) == str(seller_oid):
                            seller_items.append({
                                "product_id": str(item.product.id),
                                "product_name": item.product.name,
                                "quantity": int(item.quantity),
                                "price": float(item.product.price),
                                "image": item.product.image_url
                            })
                except Exception:
                    continue

            if seller_items:
                result.append({
                    "id": str(order.id),
                    "buyer": {
                        "id": str(order.user.id) if order.user else "Unknown",
                        "username": order.user.username if order.user else "Unknown User"
                    },
                    "items": seller_items,
                    "items_count": len(seller_items),
                    "total_price": sum(i["price"] * i["quantity"] for i in seller_items),
                    "status": order.status,
                    "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S") if order.created_at else "N/A"
                })

        return jsonify({"orders": result, "total": len(result)}), 200

    except Exception as e:
        print("Detailed Error in get_seller_orders:", str(e)) 
        return jsonify({"msg": f"Backend Error: {str(e)}"}), 500