from flask import Blueprint, jsonify, request, abort, make_response
from models import db
from models.review import Review
from flask_login import current_user

review_view = Blueprint('review_view', __name__)

@review_view.route('/reviews', methods=['POST'])
def create_review():
    """
    Create a new review for a vendor.

    Request Body:
    - vendor_id (str): ID of the vendor being reviewed.
    - rating (int): Rating given in the review (1-5).
    - comment (str): Comment or feedback in the review.

    Returns:
    - JSON object representing the created review.
    """
    data = request.get_json()

    # Validate required fields
    if not data or not 'vendor_id' in data or not 'rating' in data or not 'comment' in data:
        abort(400, description="Missing required fields")

    # Create a new review
    new_review = Review(
        vendor_id=data['vendor_id'],
        user_id=current_user.id,
        rating=data['rating'],
        comment=data['comment']
    )
    db.session.add(new_review)
    db.session.commit()

    return make_response(jsonify(new_review.to_dict()), 201)

@review_view.route('/reviews/<string:review_id>', methods=['GET'])
def get_review(review_id):
    """
    Retrieve a specific review by ID.

    Path Parameters:
    - review_id (str): ID of the review to retrieve.

    Returns:
    - JSON object representing the review.
    """
    review = Review.query.get(review_id)
    if not review:
        abort(404, description="Review not found")
    return jsonify(review.to_dict()), 200

@review_view.route('/reviews/<string:review_id>', methods=['PUT'])
def update_review(review_id):
    """
    Update a review by ID.

    Path Parameters:
    - review_id (str): ID of the review to update.

    Request Body:
    - rating (int): Updated rating given in the review (1-5).
    - comment (str): Updated comment or feedback in the review.

    Returns:
    - JSON object representing the updated review.
    """
    review = Review.query.get(review_id)
    if not review:
        abort(404, description="Review not found")

    data = request.get_json()
    review.update(**data)
    db.session.commit()

    return jsonify(review.to_dict()), 200

@review_view.route('/reviews/<string:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """
    Delete a review by ID.

    Path Parameters:
    - review_id (str): ID of the review to delete.

    Returns:
    - JSON object with a success message.
    """
    review = Review.query.get(review_id)
    if not review:
        abort(404, description="Review not found")

    db.session.delete(review)
    db.session.commit()

    return jsonify({'message': 'Review deleted successfully'}), 200
