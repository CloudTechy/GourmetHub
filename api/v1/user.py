""" This represents the user API endpoint """

from flask import abort, request, jsonify, make_response, Blueprint
from models import db
from models.user import User
from flask_login import login_required
from werkzeug.security import generate_password_hash

user_api = Blueprint('user_api', __name__)

@user_api.route('users', methods=['POST', 'GET'])
def users():
    if request.method == 'POST':
        data = request.get_json()
        
        if not data or not 'email' in data or not 'password' in data:
            abort(400, description="Missing email or password")

        if User.query.filter_by(email=data['email']).first():
            abort(400, description="User already exists")

        data['password'] = generate_password_hash(data['password'], method='sha256')
        user = User(**data)
        user.save()
        return make_response(jsonify(user.to_dict()), 201)
    else:
        users = User.query.all()
        users = [user.to_dict() for user in users]
        return make_response(jsonify(users), 200)

@user_api.route('users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(404, description="User not found")
    if request.method == 'GET':
        return make_response(jsonify(user.to_dict()), 200)
    elif request.method == 'PUT':
        data = request.get_json()
        user.update(**data)
        return make_response(jsonify(user.to_dict()), 200)
    elif request.method == 'DELETE':
        user.delete()
        return make_response(jsonify({'message': 'success'}), 200)
