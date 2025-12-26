from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from bson import ObjectId
from functools import wraps

from models import User, Product, Order

admin = Blueprint('admin', __name__)

# ===== Hardcoded Admin Credentials =====
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


def admin_required(fn):
    """Decorator to check if user is admin"""
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.objects(id=ObjectId(user_id)).first()
        if not user or not user.is_admin:
            return jsonify({"msg": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


# -----------------------------
# Admin Login
# -----------------------------
@admin.route('/admin/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        # Find or create admin user
        admin_user = User.objects(username=ADMIN_USERNAME, is_admin=True).first()
        
        if not admin_user:
            # Create admin user if not exists
            from werkzeug.security import generate_password_hash
            admin_user = User(
                username=ADMIN_USERNAME,
                email="admin@p2ukaiser.com",
                password=generate_password_hash(ADMIN_PASSWORD),
                full_name="Administrator",
                is_admin=True,
                is_email_verified=True
            )
            admin_user.save()
        
        access_token = create_access_token(identity=str(admin_user.id))
        return jsonify({
            "access_token": access_token,
            "user": {
                "id": str(admin_user.id),
                "username": admin_user.username,
                "is_admin": True
            }
        }), 200
    
    return jsonify({"msg": "Invalid admin credentials"}), 401


# -----------------------------
# Get Dashboard Statistics
# -----------------------------
@admin.route('/admin/stats', methods=['GET'])
@admin_required
def get_stats():
    total_users = User.objects(is_admin__ne=True).count()
    total_sellers = User.objects(is_seller=True).count()
    total_products = Product.objects.count()
    total_orders = Order.objects.count()
    
    # Calculate total revenue
    orders = Order.objects(status='completed')
    total_revenue = sum(float(order.total_price) for order in orders)
    
    # Recent orders
    recent_orders = Order.objects.order_by('-created_at').limit(10)
    recent_orders_list = []
    for order in recent_orders:
        recent_orders_list.append({
            "id": str(order.id),
            "user": order.user.username if order.user else "Unknown",
            "total": float(order.total_price),
            "status": order.status,
            "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    
    return jsonify({
        "total_users": total_users,
        "total_sellers": total_sellers,
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "recent_orders": recent_orders_list
    }), 200


# -----------------------------
# Get All Users
# -----------------------------
@admin.route('/admin/users', methods=['GET'])
@admin_required
def get_all_users():
    users = User.objects(is_admin__ne=True)
    users_list = []
    for user in users:
        users_list.append({
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_seller": user.is_seller,
            "is_active": user.is_active,
            "coin_balance": user.coin_balance,
            "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(users_list), 200


# -----------------------------
# Ban/Unban User
# -----------------------------
@admin.route('/admin/users/<user_id>/toggle-ban', methods=['PUT'])
@admin_required
def toggle_ban_user(user_id):
    try:
        user = User.objects.get(id=ObjectId(user_id))
        user.is_active = not user.is_active
        user.save()
        return jsonify({
            "msg": f"User {'unbanned' if user.is_active else 'banned'} successfully",
            "is_active": user.is_active
        }), 200
    except:
        return jsonify({"msg": "User not found"}), 404


# -----------------------------
# Delete User
# -----------------------------
@admin.route('/admin/users/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    try:
        user = User.objects.get(id=ObjectId(user_id))
        # Delete user's products
        Product.objects(seller=user).delete()
        user.delete()
        return jsonify({"msg": "User deleted successfully"}), 200
    except:
        return jsonify({"msg": "User not found"}), 404


# -----------------------------
# Get All Products (Admin)
# -----------------------------
@admin.route('/admin/products', methods=['GET'])
@admin_required
def get_all_products_admin():
    products = Product.objects.order_by('-created_at')
    products_list = []
    for p in products:
        products_list.append({
            "id": str(p.id),
            "name": p.name,
            "price": float(p.price),
            "image_url": p.image_url,
            "seller": {
                "id": str(p.seller.id),
                "username": p.seller.username
            } if p.seller else None,
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(products_list), 200


# -----------------------------
# Delete Product (Admin)
# -----------------------------
@admin.route('/admin/products/<product_id>', methods=['DELETE'])
@admin_required
def delete_product_admin(product_id):
    try:
        product = Product.objects.get(id=ObjectId(product_id))
        product.delete()
        return jsonify({"msg": "Product deleted successfully"}), 200
    except:
        return jsonify({"msg": "Product not found"}), 404


# -----------------------------
# Get All Orders (Admin)
# -----------------------------
@admin.route('/admin/orders', methods=['GET'])
@admin_required
def get_all_orders():
    orders = Order.objects.order_by('-created_at')
    orders_list = []
    for order in orders:
        orders_list.append({
            "id": str(order.id),
            "user": {
                "id": str(order.user.id),
                "username": order.user.username
            } if order.user else None,
            "total_price": float(order.total_price),
            "status": order.status,
            "created_at": order.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(orders_list), 200


# -----------------------------
# Update Order Status (Admin)
# -----------------------------
@admin.route('/admin/orders/<order_id>/status', methods=['PUT'])
@admin_required
def update_order_status(order_id):
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status not in ['pending', 'processing', 'completed', 'cancelled']:
        return jsonify({"msg": "Invalid status"}), 400
    
    try:
        order = Order.objects.get(id=ObjectId(order_id))
        order.status = new_status
        order.save()
        return jsonify({"msg": "Order status updated", "status": new_status}), 200
    except:
        return jsonify({"msg": "Order not found"}), 404
