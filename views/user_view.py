from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db
from models.user import User
from werkzeug.security import generate_password_hash

user_view = Blueprint('user_view', __name__)

@user_view.route('/users', methods=['GET'])
def list_users():
    """
    Render a list of all users.

    Returns:
        HTML rendering of all users.
    """
    users = User.query.all()
    return render_template('users.html', users=users)

@user_view.route('/users/<string:user_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def manage_user(user_id):
    """
    Manage a user by ID.

    Args:
        user_id (str): ID of the user to manage.

    Methods:
        GET: Render user details.
        POST: Create a new user.
        PUT: Update user details.
        DELETE: Delete user.

    Returns:
        HTML rendering or redirect based on the method.
    """
    user = User.query.get_or_404(user_id)

    if request.method == 'GET':
        return render_template('user.html', user=user)

    elif request.method == 'POST':
        data = request.form
        if not data or not data.get('email') or not data.get('password'):
            flash('Email and password are required fields', 'error')
            return redirect(url_for('manage_user', user_id=user_id))
        
        if User.query.filter_by(email=data['email']).first():
            flash('User with this email already exists', 'error')
            return redirect(url_for('manage_user', user_id=user_id))
        
        data['password'] = generate_password_hash(data['password'], method='sha256')
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('list_users'))

    elif request.method == 'PUT':
        data = request.form
        if not data or not data.get('email'):
            flash('Email is required to update user details', 'error')
            return redirect(url_for('manage_user', user_id=user_id))

        user.update(**data)
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('manage_user', user_id=user_id))

    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
        return redirect(url_for('list_users'))
