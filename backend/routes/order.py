from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Order, User
from mongoengine import Document, ReferenceField, ListField
from bson import ObjectId

order = Blueprint('order', __name__)

#  - - - -Order Model --  --  -
class Order_item(Document):
    user = ReferenceField(User, required=True, unique=True)
    order = ListField(ReferenceField(Order))

# This function is no longer called by the refactored endpoints, but is kept for reference.
def count_Order_for_Order(order_ids):
    counts = {}
    for order_id in order_ids:
        counts[order_id] = Order.objects(order=ObjectId(order_id)).count()
    return counts


# 🔹 Get all order of the current user
@order.route('/order', methods=['GET'])
@jwt_required()
def get_order():
    return jsonify({"msg": "Data retrieval successful"})

# 🔹 Create a new note
@order.route('/order', methods=['POST'])
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()
    user = User.objects(id=ObjectId(user_id)).first()

    order = Order(
        items=data['Items'],
        total_price=float(data.get('Price', '')),
        status=data.get('Status', ''),
        user=user
    )
    order.save()

    return jsonify({"msg": "Note created!"})


# 🔹 Update note by ID
@order.route('/order/<order_id>', methods=['PUT'])
@jwt_required()
def update_note(order_id):
    data = request.get_json()
    update_data = {}

    if 'Item' in data:
        update_data['Item'] = data['Item']
    if 'Price' in data:
        update_data['Price'] = data['Price']
    if 'Status' in data:
        update_data['Status'] = data['Status']

    Order.objects(id=ObjectId(order_id)).update_one(**update_data)
    return jsonify({"msg": "Note updated!"})

# 🔹 Delete note by ID
@order.route('/notes/<order_id>', methods=['DELETE'])
@jwt_required()
def delete_note(order_id):
    Order.objects(id=ObjectId(order_id)).delete()
    return jsonify({"msg": "Note deleted!"})