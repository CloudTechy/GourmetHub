from flask import Flask, jsonify, render_template, redirect, url_for, request, flash
from models import db
from models.user import User
# from api.v1.user import user_api  # Import the user_view blueprint
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from route import register_blueprints
# from flask_restful import Api
app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gourmethub.db'

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth_view.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Initialize Flask-RESTful
# api = Api(app)

# Register all blueprints here
register_blueprints(app, '/api/v1')

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Resource not found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)