from flask import Flask, jsonify, render_template, redirect, url_for, request, flash, send_from_directory
from models import db
from models.user import User
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from route import register_blueprints
from flask_cors import CORS 
from datetime import datetime
from jinja2 import Environment
from os import getenv, path
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)
@app.context_processor
def inject_now():
    return {'datetime': datetime}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URI', 'sqlite:///db.sqlite3')

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'views.auth_view.login'

# Initialize Flask-Migrate
migrate = Migrate(app, db)


# Initialize Flask-RESTful
# api = Api(app)

#Enable CORS
CORS(app, resources={r"/*": {"origins": "*"}})


# Register all blueprints here
register_blueprints(app)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(path.join(app.root_path, 'static/images'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)