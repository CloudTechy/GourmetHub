from flask import Blueprint, request, jsonify, abort
from models import db
from models.order import Order
from models.food_item import FoodItem
from models.order_item import OrderItem
from flask_login import current_user, login_required

order_view = Blueprint('order_view', __name__)

@order_view.route('/orders', methods=['POST'])
@login_required
def create_order():
    """
    Create a new order.

    JSON Payload:
    {
        "food_items": [
            {"fooditem_id": "<fooditem_id>", "quantity": <quantity>}
        ]
    }

    Returns:
        JSON response with order details or error message.
    """
    data = request.get_json()
    food_items = data.get('food_items')

    if not food_items:
        abort(400, description="Missing food items")

    total_price = 0
    vendor_id = None

    for item in food_items:
        food_item = FoodItem.query.get(item['fooditem_id'])
        if not food_item:
            abort(404, description=f"Food item with id {item['fooditem_id']} not found")

        if vendor_id is None:
            vendor_id = food_item.vendor_id
        elif vendor_id != food_item.vendor_id:
            abort(400, description="All food items must belong to the same vendor")

        total_price += food_item.price * item['quantity']

    order = Order(user_id=current_user.id, vendor_id=vendor_id, total_price=total_price, status='pending')
    order.save()

    for item in food_items:
        order_item = OrderItem(order_id=order.id, fooditem_id=item['fooditem_id'], quantity=item['quantity'], price=FoodItem.query.get(item['fooditem_id']).price)
        order_item.save()

    return jsonify(order.to_dict()), 201

@order_view.route('/orders/<string:order_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def manage_order(order_id):
    """
    Manage an order by ID.

    Args:
        order_id (str): ID of the order to manage.

    Methods:
        GET: Retrieve order details.
        PUT: Update order details.
        DELETE: Cancel order.

    Returns:
        JSON response with order details or error message.
    """
    order = Order.query.get(order_id)
    if not order:
        abort(404, description="Order not found")

    if request.method == 'GET':
        return jsonify(order.to_dict()), 200

    elif request.method == 'PUT':
        if current_user.id != order.user_id:
            abort(403, description="Unauthorized to update this order")

        data = request.get_json()
        if not data:
            abort(400, description="No data provided for update")

        order.status = data.get('status', order.status)
        order.update()

        return jsonify(order.to_dict()), 200

    elif request.method == 'DELETE':
        if current_user.id != order.user_id:
            abort(403, description="Unauthorized to delete this order")

        order.delete()
        return jsonify({'message': 'Order canceled successfully'}), 200

@order_view.route('/orders', methods=['GET'])
@login_required
def list_orders():
    """
    List all orders for the current user.

    Returns:
        JSON response with list of orders.
    """
    orders = Order.query.filter_by(user_id=current_user.id).all()
    orders = [order.to_dict() for order in orders]
    return jsonify(orders), 200
