from flask import Flask, jsonify, render_template, redirect, url_for, request, flash
from models import db
from models.user import User
from models.vendor import Vendor
from models.review import Review
from models.order import Order
from models.order_item import OrderItem
from models.food_item import FoodItem
from views.user import user_view  # Import the user_view blueprint

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gourmethub.db'

db.init_app(app)

app.register_blueprint(user_view, url_prefix='/api/v1')

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Resource not found"}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)