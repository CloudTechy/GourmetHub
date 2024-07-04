from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.review import Review
from models.vendor import Vendor
from flask_login import login_required, current_user

review_view = Blueprint('review_view', __name__)

@review_view.route('/reviews', methods=['GET'])
def list_reviews():
    """
    List all reviews.
    """
    reviews = Review.query.all()
    return render_template('reviews/list.html', reviews=reviews)

@review_view.route('/reviews/add', methods=['GET', 'POST'])
@login_required
def add_review():
    """
    Add a new review.
    """
    if request.method == 'POST':
        data = request.form
        if not data['vendor_id'] or not data['rating']:
            flash('Vendor ID and rating are required!', 'danger')
            return redirect(url_for('review_view.add_review'))

        review = Review(user_id=current_user.id, vendor_id=data['vendor_id'], rating=data['rating'], comment=data['comment'])
        review.save()
        flash('Review added successfully!', 'success')
        return redirect(url_for('review_view.list_reviews'))
    
    return render_template('reviews/add.html')

@review_view.route('/reviews/<string:review_id>', methods=['GET'])
def review_detail(review_id):
    """
    Display review details.
    """
    review = Review.query.get(review_id)
    if not review:
        flash('Review not found!', 'danger')
        return redirect(url_for('review_view.list_reviews'))

    return render_template('reviews/detail.html', review=review)


