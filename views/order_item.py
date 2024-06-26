from flask import Blueprint, jsonify, request, abort, make_response
from models import db
from models.order_item import OrderItem

order_item_view = Blueprint('order_item_view', __name__)

@order_item_view.route('/order_items', methods=['POST'])
def create_order_item():
    """
    Add a new item to an order.

    Request Body:
    - order_id (str): ID of the order to which the item belongs.
    - food_item_id (str): ID of the food item being ordered.
    - quantity (int): Quantity of the food item.
    - price (float): Price of the food item.

    Returns:
    - JSON object representing the created order item.
    """
    data = request.get_json()

    # Validate required fields
    if not data or not 'order_id' in data or not 'food_item_id' in data or not 'quantity' in data or not 'price' in data:
        abort(400, description="Missing required fields")

    # Create a new order item
    new_order_item = OrderItem(
        order_id=data['order_id'],
        food_item_id=data['food_item_id'],
        quantity=data['quantity'],
        price=data['price']
    )
    db.session.add(new_order_item)
    db.session.commit()

    return make_response(jsonify(new_order_item.to_dict()), 201)

@order_item_view.route('/order_items', methods=['GET'])
def get_order_items():
    """
    Retrieve all order items.

    Returns:
    - JSON array of all order items.
    """
    order_items = OrderItem.query.all()
    order_items = [item.to_dict() for item in order_items]
    return make_response(jsonify(order_items), 200)

@order_item_view.route('/order_items/<string:order_item_id>', methods=['GET'])
def get_order_item(order_item_id):
    """
    Retrieve a specific order item by ID.

    Path Parameters:
    - order_item_id (str): ID of the order item to retrieve.

    Returns:
    - JSON object representing the order item.
    """
    order_item = OrderItem.query.get(order_item_id)
    if not order_item:
        abort(404, description="Order item not found")
    return jsonify(order_item.to_dict()), 200

@order_item_view.route('/order_items/<string:order_item_id>', methods=['PUT'])
def update_order_item(order_item_id):
    """
    Update an order item by ID.

    Path Parameters:
    - order_item_id (str): ID of the order item to update.

    Request Body:
    - order_id (str): Updated ID of the order to which the item belongs.
    - food_item_id (str): Updated ID of the food item being ordered.
    - quantity (int): Updated quantity of the food item.
    - price (float): Updated price of the food item.

    Returns:
    - JSON object representing the updated order item.
    """
    order_item = OrderItem.query.get(order_item_id)
    if not order_item:
        abort(404, description="Order item not found")

    data = request.get_json()
    order_item.update(**data)
    db.session.commit()

    return jsonify(order_item.to_dict()), 200

@order_item_view.route('/order_items/<string:order_item_id>', methods=['DELETE'])
def delete_order_item(order_item_id):
    """
    Delete an order item by ID.

    Path Parameters:
    - order_item_id (str): ID of the order item to delete.

    Returns:
    - JSON object with a success message.
    """
    order_item = OrderItem.query.get(order_item_id)
    if not order_item:
        abort(404, description="Order item not found")

    db.session.delete(order_item)
    db.session.commit()

    return jsonify({'message': 'Order item deleted successfully'}), 200
