# routes/product.py
import os
import uuid
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from bson import ObjectId
from mongoengine.errors import DoesNotExist, ValidationError

from models import User, Product

product = Blueprint('product', __name__)
UPLOAD_FOLDER = 'uploads/products'

# ฟังก์ชันสำหรับตรวจสอบไฟล์ที่อัปโหลด
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# ✅ Create Product
@product.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    """
    สร้างสินค้าใหม่ โดยรับข้อมูลจาก form data และไฟล์รูปภาพ
    ต้องเป็น seller เท่านั้นถึงจะสร้างสินค้าได้
    """
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()

    if not user or not user.is_seller:
        return jsonify({"msg": "Unauthorized. Only sellers can create products."}), 403

    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    image = request.files.get('image')

    if not all([name, price]):
        return jsonify({"msg": "Product name and price are required."}), 400

    image_url = None
    if image and allowed_file(image.filename):
        try:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(image.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            new_filename = f"{uuid.uuid4().hex}.{ext}"
            save_path = os.path.join(UPLOAD_FOLDER, new_filename)
            image.save(save_path)
            image_url = f"/{UPLOAD_FOLDER}/{new_filename}"
        except Exception as e:
            return jsonify({"msg": f"Failed to upload image: {str(e)}"}), 500
    
    try:
        new_product = Product(
            name=name,
            description=description,
            price=float(price),
            image_url=image_url,
            seller=user.id
        )
        new_product.save()
        return jsonify(new_product.to_json()), 201
    except ValidationError as e:
        return jsonify({"msg": str(e)}), 400
    except ValueError:
        return jsonify({"msg": "Price must be a valid number."}), 400

# ✅ Get all products
@product.route('/products', methods=['GET'])
def get_all_products():
    """
    ดึงข้อมูลสินค้าทั้งหมด
    """
    products = Product.objects.all()
    # ดึงข้อมูล seller มาด้วย
    product_list = [p.to_json() for p in products]
    return jsonify(product_list), 200

# ✅ Get a single product
@product.route('/products/<string:product_id>', methods=['GET'])
def get_product(product_id):
    """
    ดึงข้อมูลสินค้าเฉพาะรายการ
    """
    try:
        product_item = Product.objects.get(id=ObjectId(product_id))
        return jsonify(product_item.to_json()), 200
    except (DoesNotExist, ValidationError):
        return jsonify({"msg": "Product not found."}), 404

# ✅ Delete product
@product.route('/products/<string:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """
    ลบสินค้า ต้องเป็น seller ที่สร้างสินค้านั้นเท่านั้น
    """
    user_id = get_jwt_identity()

    try:
        product_item = Product.objects.get(id=ObjectId(product_id))
    except (DoesNotExist, ValidationError):
        return jsonify({"msg": "Product not found."}), 404

    # ตรวจสอบว่าผู้ใช้ที่ล็อกอินอยู่เป็นเจ้าของสินค้าหรือไม่
    if str(product_item.seller.id) != user_id:
        return jsonify({"msg": "Unauthorized. You can only delete your own products."}), 403

    try:
        product_item.delete()
        return jsonify({"msg": "Product deleted successfully."}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500
