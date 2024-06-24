""" This represents the user api endpoint """

from flask import abort, request, jsonify, make_response, Blueprint
from models import db
from models.user import User

user_view = Blueprint('user_view', __name__)

@user_view.route('users', methods=['POST', 'GET'])
def users():
    if request.method == 'POST':
        data = request.get_json()
        user = User(**data)
        user.save()
        return make_response(jsonify(user.to_dict()), 201)
    else:
        users = User.query.all()
        users = [user.to_dict() for user in users]
        return make_response(jsonify(users), 200)

@user_view.route('users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        abort(404)
    if request.method == 'GET':
        return make_response(jsonify(user.to_dict()), 200)
    elif request.method == 'PUT':
        data = request.get_json()
        user.update(**data)
        return make_response(jsonify(user.to_dict()), 200)
    elif request.method == 'DELETE':
        user.delete()
        return make_response(jsonify({'message':'success'}), 200)
