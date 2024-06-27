from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.vendor import Vendor
from models.food_item import FoodItem
from flask_login import login_required, current_user

vendor_view = Blueprint('vendor_view', __name__)

@vendor_view.route('/', strict_slashes=False, methods=['GET'])
def list_vendors():
    """
    List all vendors.
    """
    vendors = Vendor.query.all()
    return render_template('vendors/list.html', vendors=vendors)

@vendor_view.route('/vendors/register', methods=['GET', 'POST'])
@login_required
def register_vendor():
    """
    Register a new vendor.
    """
    if request.method == 'POST':
        data = request.form
        if not data['name'] or not data['description']:
            flash('Name and description are required!', 'danger')
            return redirect(url_for('vendor_view.register_vendor'))

        vendor = Vendor(user_id=current_user.id, name=data['name'], description=data['description'], 
                        contact_details=data['contact_details'], location=data['location'])
        vendor.save()
        flash('Vendor registered successfully!', 'success')
        return redirect(url_for('vendor_view.list_vendors'))

    return render_template('vendors/register.html')

@vendor_view.route('/vendors/<string:vendor_id>', methods=['GET'])
def vendor_detail(vendor_id):
    """
    Display vendor details and their food items.
    """
    vendor = Vendor.query.get(vendor_id)
    if not vendor:
        flash('Vendor not found!', 'danger')
        return redirect(url_for('vendor_view.list_vendors'))

    food_items = FoodItem.query.filter_by(vendor_id=vendor_id).all()
    return render_template('vendors/detail.html', vendor=vendor, food_items=food_items)

@vendor_view.route('/vendors/<string:vendor_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_vendor(vendor_id):
    """
    Edit vendor details.
    """
    vendor = Vendor.query.get(vendor_id)
    if not vendor:
        flash('Vendor not found!', 'danger')
        return redirect(url_for('vendor_view.list_vendors'))

    if request.method == 'POST':
        data = request.form
        vendor.update(name=data['name'], description=data['description'], 
                      contact_details=data['contact_details'], location=data['location'])
        flash('Vendor updated successfully!', 'success')
        return redirect(url_for('vendor_view.vendor_detail', vendor_id=vendor.id))

    return render_template('vendors/edit.html', vendor=vendor)

@vendor_view.route('/vendors/<string:vendor_id>/delete', methods=['POST'])
@login_required
def delete_vendor(vendor_id):
    """
    Delete a vendor.
    """
    vendor = Vendor.query.get(vendor_id)
    if not vendor:
        flash('Vendor not found!', 'danger')
        return redirect(url_for('vendor_view.list_vendors'))

    vendor.delete()
    flash('Vendor deleted successfully!', 'success')
    return redirect(url_for('vendor_view.list_vendors'))
