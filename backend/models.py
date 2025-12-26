from mongoengine import (
    Document, StringField, EmailField, BooleanField, DateTimeField,
    ListField, EmbeddedDocument, EmbeddedDocumentField, ReferenceField,
    DecimalField, FloatField, CASCADE, IntField
)
from datetime import datetime


# -------- Topup Transaction Model (Embedded) --------
class TopupTransaction(EmbeddedDocument):
    transaction_id = StringField(required=True)
    method = StringField(required=True, choices=["omise", "promptpay", "truemoney"])
    amount = IntField(required=True)  # จำนวนเงิน (บาท) = Coin
    status = StringField(default='pending', choices=["pending", "success", "failed"])
    created_at = DateTimeField(default=datetime.utcnow)


# -------- Address Model --------
class Address(EmbeddedDocument):
    name = StringField(required=True)
    phone = StringField(required=True)
    address_line = StringField(required=True)
    district = StringField(required=True)
    province = StringField(required=True)
    postal_code = StringField(required=True)
    is_default = BooleanField(default=False)


# -------- User Model --------
class User(Document):
    username = StringField(required=True, unique=True, min_length=4, max_length=20)
    email = EmailField(required=True, unique=True)
    password = StringField(required=True)
    profile_image_url = StringField()

    full_name = StringField(required=True)
    phone_number = StringField()
    addresses = ListField(EmbeddedDocumentField(Address))

    is_seller = BooleanField(default=False)
    is_admin = BooleanField(default=False)  # Admin flag
    shop_name = StringField()
    
    is_active = BooleanField(default=True)
    is_email_verified = BooleanField(default=False)
    email_verification_token = StringField()
    email_verification_token_expiration = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)

    # Wishlist ของผู้ใช้
    wishlist = ListField(ReferenceField('Product'))

    # ===== ระบบ Coin =====
    coin_balance = IntField(default=0)  # ยอด coin คงเหลือ
    topup_transactions = ListField(EmbeddedDocumentField(TopupTransaction))

    # ===== ฟิลด์สำหรับ AI Ranking =====
    total_sales = FloatField(default=0.0)        # ยอดขายรวม
    rating_avg = FloatField(default=0.0)         # คะแนนเฉลี่ย
    delivery_speed = FloatField(default=0.0)     # วันเฉลี่ยต่อการจัดส่ง
    response_rate = FloatField(default=0.0)      # อัตราการตอบลูกค้า
    cancel_rate = FloatField(default=0.0)        # อัตราการยกเลิก
    ai_score = FloatField(default=0.0)           # คะแนนจาก AI
    ai_level = StringField(default="C")          # ระดับ (S, A, B, C)

    # ===== Gamification =====
    member_level = StringField(default="Bronze", choices=["Bronze", "Silver", "Gold", "Diamond"])
    xp = IntField(default=0)                      # Experience points
    check_in_streak = IntField(default=0)         # Current streak days
    last_check_in = DateTimeField()               # Last check-in date
    total_spent = FloatField(default=0.0)         # Total amount spent

    meta = {'collection': 'users'}


# -------- Product Model --------
class Product(Document):
    name = StringField(required=True, max_length=100)
    description = StringField()
    price = DecimalField(required=True, min_value=0)
    image_url = StringField()
    category = StringField(default='all')  # Category for filtering
    seller = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'products'}


# -------- CartItem Model --------
class CartItem(Document):
    product = ReferenceField('Product', required=True)
    quantity = DecimalField(required=True, min_value=1)
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    added_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'cart_items'}


# -------- Order Model --------
class Order(Document):
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    items = ListField(ReferenceField('CartItem'))
    total_price = DecimalField(required=True, min_value=0)
    status = StringField(default='pending')  # pending, processing, completed, cancelled
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'orders'}


# -------- Review Model --------
class Review(Document):
    product = ReferenceField('Product', required=True, reverse_delete_rule=CASCADE)
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    rating = IntField(required=True, min_value=1, max_value=5)  # 1-5 stars
    comment = StringField(max_length=500)
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'reviews'}


# -------- Notification Model --------
class Notification(Document):
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    title = StringField(required=True)
    message = StringField(required=True)
    type = StringField(default='info', choices=['info', 'order', 'review', 'promo', 'system'])
    is_read = BooleanField(default=False)
    link = StringField()  # Optional link to navigate
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'notifications'}


# -------- Conversation Model (Chat) --------
class Conversation(Document):
    participants = ListField(ReferenceField('User'), required=True)  # 2 users
    last_message = StringField()
    last_message_at = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'conversations'}


# -------- Message Model (Chat) --------
class Message(Document):
    conversation = ReferenceField('Conversation', required=True, reverse_delete_rule=CASCADE)
    sender = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    content = StringField(required=True, max_length=1000)
    is_read = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'messages'}


# -------- Mission Model --------
class Mission(Document):
    title = StringField(required=True)
    description = StringField()
    type = StringField(required=True, choices=['daily', 'weekly', 'achievement'])
    requirement_type = StringField(required=True, choices=['check_in', 'purchase', 'spend', 'review', 'order_count'])
    requirement_value = IntField(required=True)  # Target value to complete
    xp_reward = IntField(default=0)
    coin_reward = IntField(default=0)
    is_active = BooleanField(default=True)
    meta = {'collection': 'missions'}


# -------- UserMission Model --------
class UserMission(Document):
    user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    mission = ReferenceField('Mission', required=True, reverse_delete_rule=CASCADE)
    progress = IntField(default=0)
    is_completed = BooleanField(default=False)
    is_claimed = BooleanField(default=False)
    completed_at = DateTimeField()
    claimed_at = DateTimeField()
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'user_missions'}


# -------- Auction Model --------
class Auction(Document):
    title = StringField(required=True, max_length=200)
    description = StringField()
    image_url = StringField()
    category = StringField(default='all')
    starting_price = DecimalField(required=True, min_value=0)
    current_price = DecimalField(required=True, min_value=0)
    min_bid_increment = DecimalField(default=10)  # ขั้นต่ำในการเพิ่มราคา
    seller = ReferenceField('User', required=True)
    winner = ReferenceField('User')  # ผู้ชนะการประมูล
    start_time = DateTimeField(default=datetime.utcnow)
    end_time = DateTimeField(required=True)  # เวลาสิ้นสุดการประมูล
    is_active = BooleanField(default=True)
    is_ended = BooleanField(default=False)
    total_bids = IntField(default=0)
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'auctions'}


# -------- AuctionBid Model --------
class AuctionBid(Document):
    auction = ReferenceField('Auction', required=True, reverse_delete_rule=CASCADE)
    bidder = ReferenceField('User', required=True)
    amount = DecimalField(required=True, min_value=0)
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {'collection': 'auction_bids', 'ordering': ['-created_at']}
