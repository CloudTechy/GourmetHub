from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.food_item import FoodItem
from models.vendor import Vendor
from flask_login import login_required, current_user

food_item_view = Blueprint('food_item_view', __name__)

@food_item_view.route('/fooditems', methods=['GET'])
def list_fooditems():
    """
    List all food items.
    """
    fooditems = FoodItem.query.all()
    return render_template('fooditems/list.html', fooditems=fooditems)

@food_item_view.route('/fooditems/add', methods=['GET', 'POST'])
@login_required
def add_fooditem():
    """
    Add a new food item.
    """
    if request.method == 'POST':
        data = request.form
        if not data['name'] or not data['price']:
            flash('Name and price are required!', 'danger')
            return redirect(url_for('food_item_view.add_fooditem'))

        vendor = Vendor.query.filter_by(user_id=current_user.id).first()
        if not vendor:
            flash('You need to be a registered vendor to add food items!', 'danger')
            return redirect(url_for('food_item_view.add_fooditem'))

        fooditem = FoodItem(vendor_id=vendor.id, name=data['name'], description=data['description'], 
                            price=data['price'], photo_url=data['photo_url'], status=data['status'])
        fooditem.save()
        flash('Food item added successfully!', 'success')
        return redirect(url_for('food_item_view.list_fooditems'))

    return render_template('fooditems/add.html')

@food_item_view.route('/fooditems/<string:fooditem_id>', methods=['GET'])
def fooditem_detail(fooditem_id):
    """
    Display food item details.
    """
    fooditem = FoodItem.query.get(fooditem_id)
    if not fooditem:
        flash('Food item not found!', 'danger')
        return redirect(url_for('food_item_view.list_fooditems'))

    return render_template('fooditems/detail.html', fooditem=fooditem)

@food_item_view.route('/fooditems/<string:fooditem_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_fooditem(fooditem_id):
    """
    Edit food item details.
    """
    fooditem = FoodItem.query.get(fooditem_id)
    if not fooditem:
        flash('Food item not found!', 'danger')
        return redirect(url_for('food_item_view.list_fooditems'))

    if request.method == 'POST':
        data = request.form
        fooditem.update(name=data['name'], description=data['description'], 
                        price=data['price'], photo_url=data['photo_url'], status=data['status'])
        flash('Food item updated successfully!', 'success')
        return redirect(url_for('food_item_view.fooditem_detail', fooditem_id=fooditem.id))

    return render_template('fooditems/edit.html', fooditem=fooditem)

@food_item_view.route('/fooditems/<string:fooditem_id>/delete', methods=['POST'])
@login_required
def delete_fooditem(fooditem_id):
    """
    Delete a food item.
    """
    fooditem = FoodItem.query.get(fooditem_id)
    if not fooditem:
        flash('Food item not found!', 'danger')
        return redirect(url_for('food_item_view.list_fooditems'))

    fooditem.delete()
    flash('Food item deleted successfully!', 'success')
    return redirect(url_for('food_item_view.list_fooditems'))
