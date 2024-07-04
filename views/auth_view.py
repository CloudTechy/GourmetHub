from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth_view = Blueprint('auth_view', __name__)

@auth_view.route('/register', strict_slashes = False, methods=['GET', 'POST'])
def register_user():
    """
    Register a new user.
    """
    if request.method == 'POST':
        data = request.form
        if not data['email'] or not data['password']:
            flash('Email and password are required!', 'danger')
            return redirect(url_for('auth_view.register_user'))

        if User.query.filter_by(email=data['email']).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('auth_view.register_user'))

        hashed_password = generate_password_hash(data['password'], method='sha256')
        user = User(username=data['username'], email=data['email'], password=hashed_password)
        user.save()
        flash('User registered successfully!', 'success')
        return redirect(url_for('auth_view.login_auth_view'))

    return render_template('users/register.html')

@auth_view.route('/login', strict_slashes = False, methods=['GET', 'POST'])
def login_auth_view():
    """
    Log in an existing user.
    """
    if request.method == 'POST':
        data = request.form
        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password, data['password']):
            login_user(user)
            return redirect(url_for('home'))

        flash('Invalid email or password!', 'danger')
        return redirect(url_for('auth_view.login_auth_view'))

    return render_template('users/login.html')

@auth_view.route('/logout', strict_slashes = False,)
@login_required
def logout_auth_view():
    """
    Log out the current user.
    """
    logout_user()
    return redirect(url_for('auth_view.login_auth_view'))
