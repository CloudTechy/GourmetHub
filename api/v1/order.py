from flask import Blueprint, jsonify, request, abort, make_response
from models import db
from models.order import Order
from flask_login import current_user

order_api = Blueprint('order_api', __name__)

@order_api.route('/orders', methods=['POST'])
def create_order():
    """
    Place a new order.

    Request Body:
    - vendor_id (str): ID of the vendor from which the order is placed.
    - total_price (float): Total price of the order.
    - status (str, optional): Status of the order (pending/confirmed/shipped/delivered/canceled).

    Returns:
    - JSON object representing the created order.
    """
    data = request.get_json()

    # Validate required fields
    if not data or not 'vendor_id' in data or not 'total_price' in data:
        abort(400, description="Missing required fields")

    # Create a new order
    new_order = Order(
        vendor_id=data['vendor_id'],
        user_id=current_user.id,
        total_price=data['total_price'],
        status=data.get('status', 'pending')
    )
    new_order.save()

    return make_response(jsonify(new_order.to_dict()), 201)

@order_api.route('/orders', methods=['GET'])
def get_orders():
    """
    Retrieve all orders.

    Returns:
    - JSON array of all orders.
    """
    orders = Order.query.all()
    orders = [order.to_dict() for order in orders]
    return make_response(jsonify(orders), 200)

@order_api.route('/orders/<string:order_id>', methods=['GET'])
def get_order(order_id):
    """
    Retrieve a specific order by ID.

    Path Parameters:
    - order_id (str): ID of the order to retrieve.

    Returns:
    - JSON object representing the order.
    """
    order = Order.query.get(order_id)
    if not order:
        abort(404, description="Order not found")
    return jsonify(order.to_dict()), 200

@order_api.route('/orders/<string:order_id>', methods=['PUT'])
def update_order(order_id):
    """
    Update an order by ID.

    Path Parameters:
    - order_id (str): ID of the order to update.

    Request Body:
    - status (str): Updated status of the order (pending/confirmed/shipped/delivered/canceled).

    Returns:
    - JSON object representing the updated order.
    """
    order = Order.query.get(order_id)
    if not order:
        abort(404, description="Order not found")

    data = request.get_json()
    order.update(**data)

    return jsonify(order.to_dict()), 200

@order_api.route('/orders/<string:order_id>', methods=['DELETE'])
def delete_order(order_id):
    """
    Delete an order by ID.

    Path Parameters:
    - order_id (str): ID of the order to delete.

    Returns:
    - JSON object with a success message.
    """
    order = Order.query.get(order_id)
    if not order:
        abort(404, description="Order not found")

    order.delete()

    return jsonify({'message': 'Order deleted successfully'}), 200
