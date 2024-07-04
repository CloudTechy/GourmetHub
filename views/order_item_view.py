from flask import Blueprint, request, jsonify, abort
from models import db
from models.order_item import OrderItem
from models.order import Order
from models.food_item import FoodItem
from flask_login import current_user, login_required

order_item_view = Blueprint('order_item_view', __name__)

@order_item_view.route('/orderitems', methods=['POST'])
@login_required
def create_order_item():
    """
    Create a new order item.

    JSON Payload:
    {
        "order_id": "<order_id>",
        "fooditem_id": "<fooditem_id>",
        "quantity": <quantity>
    }

    Returns:
        JSON response with order item details or error message.
    """
    data = request.get_json()
    order_id = data.get('order_id')
    fooditem_id = data.get('fooditem_id')
    quantity = data.get('quantity')

    if not order_id or not fooditem_id or not quantity:
        abort(400, description="Missing required fields: order_id, fooditem_id, quantity")

    order = Order.query.get(order_id)
    if not order:
        abort(404, description="Order not found")

    food_item = FoodItem.query.get(fooditem_id)
    if not food_item:
        abort(404, description="Food item not found")

    if order.vendor_id != food_item.vendor_id:
        abort(400, description="Food item does not belong to the vendor of the order")

    order_item = OrderItem(order_id=order_id, fooditem_id=fooditem_id, quantity=quantity, price=food_item.price)
    order_item.save()

    return jsonify(order_item.to_dict()), 201

@order_item_view.route('/orderitems/<string:orderitem_id>', methods=['GET', 'PUT', 'DELETE'])
@login_required
def manage_order_item(orderitem_id):
    """
    Manage an order item by ID.

    Args:
        orderitem_id (str): ID of the order item to manage.

    Methods:
        GET: Retrieve order item details.
        PUT: Update order item details.
        DELETE: Delete order item.

    Returns:
        JSON response with order item details or error message.
    """
    order_item = OrderItem.query.get(orderitem_id)
    if not order_item:
        abort(404, description="Order item not found")

    if request.method == 'GET':
        return jsonify(order_item.to_dict()), 200

    elif request.method == 'PUT':
        if current_user.id != order_item.order.user_id:
            abort(403, description="Unauthorized to update this order item")

        data = request.get_json()
        if not data:
            abort(400, description="No data provided for update")

        order_item.quantity = data.get('quantity', order_item.quantity)
        order_item.update()

        return jsonify(order_item.to_dict()), 200

    elif request.method == 'DELETE':
        if current_user.id != order_item.order.user_id:
            abort(403, description="Unauthorized to delete this order item")

        order_item.delete()
        return jsonify({'message': 'Order item deleted successfully'}), 200
