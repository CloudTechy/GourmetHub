import os
from flask import Flask, jsonify, render_template, redirect, url_for, request, flash
from models import db
from datetime import timedelta
from models.user import User
from werkzeug.exceptions import BadRequest, Unauthorized
# from api.v1.user import user_api  # Import the user_view blueprint
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from route import register_blueprints
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

load_dotenv()

# from flask_restful import Api
app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', )
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))
app.config['JWT_ALGORITHM'] = os.getenv('JWT_ALGORITHM', 'HS256') 

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth_view.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

#initialize the JWTManager
jwt = JWTManager(app)

# Initialize Flask-RESTful
# api = Api(app)

# Register all blueprints here
register_blueprints(app, '/api/v1')

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(error=str(e.description)), 404

@app.errorhandler(BadRequest)
def bad_request(e):
    return jsonify(error=str(e.description)), e.code

@app.errorhandler(401)
def bad_request(e):
    return jsonify(error=str(e.description)), 401

@app.errorhandler(415)
def bad_request(e):
    return jsonify(error=str(e.description)), 415

if __name__ == '__main__':
    # with app.app_context():
        # db.create_all()

    app.run(debug=True)