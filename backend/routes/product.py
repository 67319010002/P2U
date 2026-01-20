import os
import uuid
import json
import random  # <--- [เพิ่ม] ไว้สุ่มเลข Stock ตอน Seed
from flask import Blueprint, request, jsonify, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from bson import ObjectId
from mongoengine.errors import DoesNotExist, ValidationError

from models import User, Product
from mongoengine.queryset.visitor import Q

product = Blueprint('product', __name__)
UPLOAD_FOLDER = os.path.join('static', 'products')

# -----------------------------
# ตรวจสอบไฟล์ที่อนุญาตให้อัปโหลด
# -----------------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

# -----------------------------
# สร้างสินค้าใหม่ (เฉพาะ seller)
# -----------------------------
@product.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    user_id = get_jwt_identity()
    user = User.objects(id=ObjectId(user_id)).first()

    if not user or not user.is_seller:
        return jsonify({"msg": "Unauthorized. Only sellers can create products."}), 403

    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    stock = request.form.get('stock', 1)  # <--- [เพิ่ม] รับค่า stock (Default 1)
    image = request.files.get('image')
    
    # --- ส่วนรับหมวดหมู่ ---
    category_single = request.form.get('category')
    categories_str = request.form.get('categories')
    
    categories_list = []
    if categories_str:
        try:
            categories_list = json.loads(categories_str)
        except:
            categories_list = []
    
    if not categories_list and category_single:
        categories_list = [category_single]
    # ---------------------

    if not all([name, price]):
        return jsonify({"msg": "Product name and price are required."}), 400

    # แปลง Stock เป็น Int
    try:
        stock = int(stock)
        if stock < 0: stock = 0
    except ValueError:
        return jsonify({"msg": "Stock must be a valid integer."}), 400

    image_url = None
    if image and allowed_file(image.filename):
        try:
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            filename = secure_filename(image.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            new_filename = f"{uuid.uuid4().hex}.{ext}"
            save_path = os.path.join(UPLOAD_FOLDER, new_filename)
            image.save(save_path)
            image_url = url_for('static', filename=f'products/{new_filename}', _external=True)
        except Exception as e:
            return jsonify({"msg": f"Failed to upload image: {str(e)}"}), 500

    try:
        new_product = Product(
            name=name,
            description=description,
            price=float(price),
            stock=stock,                    # <--- [เพิ่ม] บันทึก Stock
            image_url=image_url,
            seller=user,
            category=category_single,
            categories=categories_list
        )
        new_product.save()

        return jsonify({
            "id": str(new_product.id),
            "name": new_product.name,
            "description": new_product.description,
            "price": float(new_product.price),
            "stock": new_product.stock,     # <--- [เพิ่ม] ส่งกลับ
            "image_url": new_product.image_url,
            "category": new_product.category,
            "categories": new_product.categories,
            "seller": {
                "id": str(user.id),
                "username": user.username,
                "shop_name": user.shop_name
            },
            "created_at": new_product.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }), 201

    except ValidationError as e:
        return jsonify({"msg": str(e)}), 400
    except ValueError:
        return jsonify({"msg": "Price must be a valid number."}), 400

# -----------------------------
# ดึงสินค้าทั้งหมด (รองรับการค้นหา)
# -----------------------------
@product.route('/products', methods=['GET'])
def get_all_products():
    search_query = request.args.get('q', '').strip()
    
    if search_query:
        products = Product.objects(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        ).order_by('-created_at')
    else:
        products = Product.objects.order_by('-created_at')
    
    product_list = []

    for p in products:
        cats = p.categories if hasattr(p, 'categories') and p.categories else []
        if not cats and p.category:
            cats = [p.category]

        # เช็ค field stock (เผื่อข้อมูลเก่าไม่มี field นี้)
        current_stock = getattr(p, 'stock', 0)

        product_list.append({
            "id": str(p.id),
            "name": p.name,
            "description": p.description,
            "price": float(p.price),
            "stock": current_stock,         # <--- [เพิ่ม] ส่งค่า Stock
            "image_url": p.image_url,
            "category": p.category or 'all',
            "categories": cats,
            "seller": {
                "id": str(p.seller.id),
                "username": p.seller.username,
                "shop_name": p.seller.shop_name
            },
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(product_list), 200

# -----------------------------
# ดึงสินค้าเดี่ยว
# -----------------------------
@product.route('/products/<string:product_id>', methods=['GET'])
def get_product(product_id):
    try:
        p = Product.objects.get(id=ObjectId(product_id))
        
        cats = p.categories if hasattr(p, 'categories') and p.categories else []
        if not cats and p.category:
            cats = [p.category]

        return jsonify({
            "id": str(p.id),
            "name": p.name,
            "description": p.description,
            "price": float(p.price),
            "stock": getattr(p, 'stock', 0), # <--- [เพิ่ม]
            "image_url": p.image_url,
            "category": p.category,
            "categories": cats,
            "seller": {
                "id": str(p.seller.id),
                "username": p.seller.username,
                "shop_name": p.seller.shop_name
            },
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }), 200
    except (DoesNotExist, ValidationError):
        return jsonify({"msg": "Product not found."}), 404

# -----------------------------
# ลบสินค้า (เฉพาะ seller เจ้าของ)
# -----------------------------
@product.route('/products/<string:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    user_id = get_jwt_identity()

    try:
        product_item = Product.objects.get(id=ObjectId(product_id))
    except (DoesNotExist, ValidationError):
        return jsonify({"msg": "Product not found."}), 404

    if str(product_item.seller.id) != user_id:
        return jsonify({"msg": "Unauthorized. You can only delete your own products."}), 403

    try:
        if product_item.image_url:
            filename = os.path.basename(product_item.image_url)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.exists(file_path):
                os.remove(file_path)

        product_item.delete()
        return jsonify({"msg": "Product deleted successfully."}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


# -----------------------------
# Seed Products (Delete old, add new)
# -----------------------------
@product.route('/products/seed', methods=['POST'])
def seed_products():
    """Delete all products and create new demo products with AI images and Stock"""
    demo_seller = User.objects(username="P2UKAISER_Shop").first()
    if not demo_seller:
        from werkzeug.security import generate_password_hash
        demo_seller = User(
            username="P2UKAISER_Shop",
            email="shop@p2ukaiser.com",
            password=generate_password_hash("shop123"),
            full_name="P2UKAISER Official Shop",
            is_seller=True,
            shop_name="P2UKAISER Official",
            is_email_verified=True
        )
        demo_seller.save()
    
    Product.objects.delete()
    
    # [แก้ไข] เพิ่ม stock เข้าไปในข้อมูลจำลอง
    products_data = [
        {
            "name": "iPhone 16 Pro Max",
            "description": "สมาร์ทโฟนรุ่นล่าสุด จอ 6.7 นิ้ว กล้อง 48MP ชิป A18 Pro",
            "price": 49900,
            "stock": 10,  # มีของ
            "category": "electronics",
            "image_url": "/static/products/product_iphone_1766769641862.png"
        },
        {
            "name": "Sony WH-1000XM5",
            "description": "หูฟังไร้สาย Noise Cancelling คุณภาพระดับพรีเมียม",
            "price": 12990,
            "stock": 5,   # มีของน้อย
            "category": "electronics",
            "image_url": "/static/products/product_headphones_1766769657879.png"
        },
        {
            "name": "Nike Air Max Pink",
            "description": "รองเท้าวิ่งสุดเท่ น้ำหนักเบา ดีไซน์สวย",
            "price": 4590,
            "stock": 0,   # สินค้าหมด (Test สีแดง)
            "category": "fashion",
            "image_url": "/static/products/product_sneakers_1766769676542.png"
        },
        {
            "name": "Apple Watch Ultra 2",
            "description": "สมาร์ทวอทช์สำหรับนักผจญภัย GPS + LTE แบตอึด",
            "price": 31900,
            "stock": 8,
            "category": "electronics",
            "image_url": "/static/products/product_watch_1766769694809.png"
        },
        {
            "name": "Minimalist Backpack",
            "description": "กระเป๋าเป้สไตล์มินิมอล กันน้ำ ใส่โน๊ตบุ๊คได้",
            "price": 1990,
            "stock": 20,
            "category": "fashion",
            "image_url": "/static/products/product_backpack_1766769712117.png"
        },
        {
            "name": "Razer DeathAdder V3 Pro",
            "description": "เมาส์เกมมิ่งไร้สาย เซนเซอร์ 30K DPI RGB",
            "price": 4990,
            "stock": 0,  # สินค้าหมด
            "category": "gaming",
            "image_url": "/static/products/product_gaming_mouse_1766769731233.png"
        },
        {
            "name": "MacBook Pro M3",
            "description": "โน้ตบุ๊คประสิทธิภาพสูง ชิป M3 Pro RAM 18GB",
            "price": 89900,
            "stock": 3,
            "category": "electronics",
            "image_url": "/static/products/product_macbook_1766770139240.png"
        },
        {
            "name": "PS5 Slim",
            "description": "เครื่องเล่นเกมรุ่นใหม่ พร้อมคอนโทรลเลอร์ DualSense",
            "price": 18990,
            "stock": 15,
            "category": "gaming",
            "image_url": "/static/products/product_ps5_1766770153698.png"
        },
        {
            "name": "เสื้อยืด Oversized",
            "description": "เสื้อยืดผ้าคอตตอน 100% สวมสบาย มีหลายสี",
            "price": 390,
            "stock": 100,
            "category": "fashion",
            "image_url": "/static/products/product_tshirt_1766770253429.png"
        },
        {
            "name": "ลิปสติก MAC Ruby Woo",
            "description": "ลิปสติกสีแดงคลาสสิค เนื้อแมท ติดทน",
            "price": 890,
            "stock": 50,
            "category": "beauty",
            "image_url": "/static/products/product_lipstick_1766770192997.png"
        },
        {
            "name": "กระทะไฟฟ้า Philips",
            "description": "กระทะไฟฟ้าเคลือบเซรามิก ทำอาหารง่าย",
            "price": 1290,
            "stock": 12,
            "category": "home",
            "image_url": "/static/products/product_pan_1766770209597.png"
        },
        {
            "name": "ลูกฟุตบอล Adidas",
            "description": "ลูกฟุตบอลหนัง PU คุณภาพสูง เบอร์ 5",
            "price": 790,
            "stock": 30,
            "category": "sports",
            "image_url": "/static/products/product_football_1766770226683.png"
        },
    ]
    
    created = []
    for p in products_data:
        cat_val = p.get("category", "all")
        # ใช้ stock ที่กำหนด หรือสุ่มเอาถ้ารายการไหนลืมใส่
        stock_val = p.get("stock", random.randint(0, 20))
        
        new_product = Product(
            name=p["name"],
            description=p["description"],
            price=p["price"],
            stock=stock_val,            # <--- [เพิ่ม]
            image_url=p["image_url"],
            seller=demo_seller,
            category=cat_val,
            categories=[cat_val]
        )
        new_product.save()
        created.append(f"{p['name']} (Stock: {stock_val})")
    
    return jsonify({
        "msg": f"Created {len(created)} products",
        "products": created
    }), 201