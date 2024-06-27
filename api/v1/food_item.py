from flask import Blueprint, jsonify, request, abort, make_response
from models import db
from models.food_item import FoodItem

food_item_api = Blueprint('food_item_api', __name__)

@food_item_api.route('/food_items', methods=['POST'])
def create_food_item():
    """
    Create a new food item.

    Request Body:
    - vendor_id (str): ID of the vendor associated with the food item.
    - name (str): Name of the food item.
    - description (str, optional): Description of the food item.
    - price (float): Price of the food item.
    - photo_url (str, optional): URL of the food item's photo.
    - status (str, optional): Status of the food item (active/inactive).

    Returns:
    - JSON object representing the created food item.
    """
    data = request.get_json()

    # Validate required fields
    if not data or not 'vendor_id' in data or not 'name' in data or not 'price' in data:
        abort(400, description="Missing required fields")

    # Create a new food item
    new_food_item = FoodItem(
        vendor_id=data['vendor_id'],
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        photo_url=data.get('photo_url'),
        status=data.get('status', 'active')
    )
    new_food_item.save()

    return make_response(jsonify(new_food_item.to_dict()), 201)

@food_item_api.route('/food_items', methods=['GET'])
def get_food_items():
    """
    Retrieve all food items.

    Returns:
    - JSON array of all food items.
    """
    food_items = FoodItem.query.all()
    food_items = [item.to_dict() for item in food_items]
    return make_response(jsonify(food_items), 200)

@food_item_api.route('/food_items/<string:food_item_id>', methods=['GET'])
def get_food_item(food_item_id):
    """
    Retrieve a specific food item by ID.

    Path Parameters:
    - food_item_id (str): ID of the food item to retrieve.

    Returns:
    - JSON object representing the food item.
    """
    food_item = FoodItem.query.get(food_item_id)
    if not food_item:
        abort(404, description="Food item not found")
    return jsonify(food_item.to_dict()), 200

@food_item_api.route('/food_items/<string:food_item_id>', methods=['PUT'])
def update_food_item(food_item_id):
    """
    Update a food item by ID.

    Path Parameters:
    - food_item_id (str): ID of the food item to update.

    Request Body:
    - vendor_id (str): Updated ID of the vendor associated with the food item.
    - name (str): Updated name of the food item.
    - description (str, optional): Updated description of the food item.
    - price (float): Updated price of the food item.
    - photo_url (str, optional): Updated URL of the food item's photo.
    - status (str, optional): Updated status of the food item (active/inactive).

    Returns:
    - JSON object representing the updated food item.
    """
    food_item = FoodItem.query.get(food_item_id)
    if not food_item:
        abort(404, description="Food item not found")

    data = request.get_json()
    food_item.update(**data)

    return jsonify(food_item.to_dict()), 200

@food_item_api.route('/food_items/<string:food_item_id>', methods=['DELETE'])
def delete_food_item(food_item_id):
    """
    Delete a food item by ID.

    Path Parameters:
    - food_item_id (str): ID of the food item to delete.

    Returns:
    - JSON object with a success message.
    """
    food_item = FoodItem.query.get(food_item_id)
    if not food_item:
        abort(404, description="Food item not found")

    food_item.delete()

    return jsonify({'message': 'Food item deleted successfully'}), 200
