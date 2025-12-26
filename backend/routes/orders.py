from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from mongoengine.errors import DoesNotExist
from datetime import datetime

from models import User, Order, CartItem, Product, Notification

orders = Blueprint('orders', __name__)


# -----------------------------
# Get User's Order History
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
                    if item_ref and item_ref.product:
                        items_list.append({
                            "product_id": str(item_ref.product.id),
                            "product_name": item_ref.product.name,
                            "product_image": item_ref.product.image_url,
                            "quantity": int(item_ref.quantity),
                            "price": float(item_ref.product.price)
                        })
                except:
                    continue
            
            result.append({
                "id": str(order.id),
                "items": items_list,
                "total_price": float(order.total_price),
                "status": order.status,
                "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S")
            })
        
        return jsonify({
            "orders": result,
            "total": len(result)
        }), 200
        
    except DoesNotExist:
        return jsonify({"msg": "User not found"}), 404


# -----------------------------
# Get Single Order Details
# -----------------------------
@orders.route('/orders/<order_id>', methods=['GET'])
@jwt_required()
def get_order_detail(order_id):
    user_id = get_jwt_identity()
    
    try:
        order = Order.objects.get(id=ObjectId(order_id))
        
        if str(order.user.id) != user_id:
            return jsonify({"msg": "Unauthorized"}), 403
        
        items_list = []
        for item_ref in order.items:
            try:
                if item_ref and item_ref.product:
                    items_list.append({
                        "product_id": str(item_ref.product.id),
                        "product_name": item_ref.product.name,
                        "product_image": item_ref.product.image_url,
                        "quantity": int(item_ref.quantity),
                        "price": float(item_ref.product.price),
                        "seller": {
                            "id": str(item_ref.product.seller.id),
                            "username": item_ref.product.seller.username,
                            "shop_name": item_ref.product.seller.shop_name
                        } if item_ref.product.seller else None
                    })
            except:
                continue
        
        return jsonify({
            "id": str(order.id),
            "items": items_list,
            "total_price": float(order.total_price),
            "status": order.status,
            "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }), 200
        
    except DoesNotExist:
        return jsonify({"msg": "Order not found"}), 404


# -----------------------------
# Create Order (Checkout)
# -----------------------------
@orders.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    cart_item_ids = data.get('cart_items', [])
    
    if not cart_item_ids:
        return jsonify({"msg": "Cart is empty"}), 400
    
    try:
        user = User.objects.get(id=ObjectId(user_id))
        
        cart_items = []
        total_price = 0
        
        for item_id in cart_item_ids:
            try:
                cart_item = CartItem.objects.get(id=ObjectId(item_id), user=user)
                cart_items.append(cart_item)
                total_price += float(cart_item.product.price) * int(cart_item.quantity)
            except:
                continue
        
        if not cart_items:
            return jsonify({"msg": "No valid cart items found"}), 400
        
        # Check if user has enough coins
        if user.coin_balance < total_price:
            return jsonify({"msg": "Insufficient coin balance"}), 400
        
        # Create order
        order = Order(
            user=user,
            items=cart_items,
            total_price=total_price,
            status='pending'
        )
        order.save()
        
        # Deduct coins
        user.coin_balance -= int(total_price)
        user.save()
        
        # Create notifications for sellers
        seller_notified = set()
        for item in cart_items:
            seller = item.product.seller
            if str(seller.id) not in seller_notified:
                Notification(
                    user=seller,
                    title="New Order",
                    message=f"You have a new order from {user.username}",
                    type="order",
                    link=f"/seller-dashboard"
                ).save()
                seller_notified.add(str(seller.id))
                
                # Update seller's total sales
                seller.total_sales += float(item.product.price) * int(item.quantity)
                seller.save()
        
        # Clear cart items after order
        for item in cart_items:
            item.delete()
        
        return jsonify({
            "msg": "Order created successfully",
            "order_id": str(order.id),
            "total_price": total_price
        }), 201
        
    except DoesNotExist:
        return jsonify({"msg": "User not found"}), 404
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


# -----------------------------
# Cancel Order (User)
# -----------------------------
@orders.route('/orders/<order_id>/cancel', methods=['PUT'])
@jwt_required()
def cancel_order(order_id):
    user_id = get_jwt_identity()
    
    try:
        order = Order.objects.get(id=ObjectId(order_id))
        
        if str(order.user.id) != user_id:
            return jsonify({"msg": "Unauthorized"}), 403
        
        if order.status != 'pending':
            return jsonify({"msg": "Can only cancel pending orders"}), 400
        
        # Refund coins
        order.user.coin_balance += int(order.total_price)
        order.user.save()
        
        order.status = 'cancelled'
        order.save()
        
        return jsonify({"msg": "Order cancelled and refunded"}), 200
        
    except DoesNotExist:
        return jsonify({"msg": "Order not found"}), 404
