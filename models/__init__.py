""" The init file for the models module. """
from os import getenv
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from models.base_model import BaseModel
from models.user import User
from models.vendor import Vendor
from models.food_item import FoodItem
from models.order import Order
from models.order_item import OrderItem
from models.review import Review
