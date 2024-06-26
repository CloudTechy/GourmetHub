from flask import Blueprint, jsonify, request, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models import db
from models.user import User

auth_api = Blueprint('auth_api', __name__)

@auth_api.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      201:
        description: User registered successfully
      400:
        description: Missing email or password / User already exists
    """
    data = request.get_json()

    if not data or not 'email' in data or not 'password' in data:
        abort(400, description="Missing email or password")

    if User.query.filter_by(email=data['email']).first():
        abort(400, description="User already exists")

    data['password'] = generate_password_hash(data['password'], method='sha256')
    user = User(**data)
    db.session.add(user)
    db.session.commit()

    return jsonify(message="User registered successfully"), 201

@auth_api.route('/login', methods=['POST'])
def login():
    """
    Authenticate user and generate JWT token.
    ---
    tags:
      - Authentication
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
            password:
              type: string
    responses:
      200:
        description: JWT access token generated successfully
      400:
        description: Missing email or password / Invalid email or password
    """
    data = request.get_json()

    if not data or not 'email' in data or not 'password' in data:
        abort(400, description="Missing email or password")

    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        abort(401, description="Invalid email or password")

    access_token = create_access_token(identity=str(user.id))
    return jsonify(access_token=access_token), 200
