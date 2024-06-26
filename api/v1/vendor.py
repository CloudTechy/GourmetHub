from flask import Blueprint, jsonify, request, abort, make_response
from models import db
from models.vendor import Vendor

vendor_api = Blueprint('vendor_api', __name__)

@vendor_api.route('/vendors', methods=['POST'])
def create_vendor():
    """
    Create a new vendor.

    Request Body:
    - name (str): Name of the vendor.
    - description (str): Description of the vendor.
    - contact_details (str, optional): Contact details of the vendor.
    - location (str, optional): Location of the vendor.

    Returns:
    - JSON object representing the created vendor.
    """
    data = request.get_json()

    # Validate required fields
    if not data or not 'name' in data or not 'description' in data:
        abort(400, description="Missing required fields")

    # Create a new vendor
    new_vendor = Vendor(
        name=data['name'],
        description=data['description'],
        contact_details=data.get('contact_details'),
        location=data.get('location')
    )
    db.session.add(new_vendor)
    db.session.commit()

    return make_response(jsonify(new_vendor.to_dict()), 201)

@vendor_api.route('/vendors', methods=['GET'])
def get_vendors():
    """
    Retrieve all vendors.

    Returns:
    - JSON array of all vendors.
    """
    vendors = Vendor.query.all()
    vendors = [vendor.to_dict() for vendor in vendors]
    return make_response(jsonify(vendors), 200)

@vendor_api.route('/vendors/<string:vendor_id>', methods=['GET'])
def get_vendor(vendor_id):
    """
    Retrieve a specific vendor by ID.

    Path Parameters:
    - vendor_id (str): ID of the vendor to retrieve.

    Returns:
    - JSON object representing the vendor.
    """
    vendor = Vendor.query.get(vendor_id)
    if not vendor:
        abort(404, description="Vendor not found")
    return jsonify(vendor.to_dict()), 200

@vendor_api.route('/vendors/<string:vendor_id>', methods=['PUT'])
def update_vendor(vendor_id):
    """
    Update a vendor by ID.

    Path Parameters:
    - vendor_id (str): ID of the vendor to update.

    Request Body:
    - name (str): Updated name of the vendor.
    - description (str): Updated description of the vendor.
    - contact_details (str, optional): Updated contact details of the vendor.
    - location (str, optional): Updated location of the vendor.

    Returns:
    - JSON object representing the updated vendor.
    """
    vendor = Vendor.query.get(vendor_id)
    if not vendor:
        abort(404, description="Vendor not found")

    data = request.get_json()
    vendor.update(**data)
    db.session.commit()

    return jsonify(vendor.to_dict()), 200

@vendor_api.route('/vendors/<string:vendor_id>', methods=['DELETE'])
def delete_vendor(vendor_id):
    """
    Delete a vendor by ID.

    Path Parameters:
    - vendor_id (str): ID of the vendor to delete.

    Returns:
    - JSON object with a success message.
    """
    vendor = Vendor.query.get(vendor_id)
    if not vendor:
        abort(404, description="Vendor not found")

    db.session.delete(vendor)
    db.session.commit()

    return jsonify({'message': 'Vendor deleted successfully'}), 200
