""" This is the Flask User Model """

from flask_login import UserMixin
from .base_model import BaseModel
from models import db
from uuid import uuid4 as uuid
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5


class User(UserMixin, BaseModel):
    """This represents the User Model """
    __tablename__ = 'users'
    first_name = db.Column(db.String(40), nullable=False)
    last_name = db.Column(db.String(40), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))
    role = db.Column(db.String(10), nullable=False, default="customer")
    vendors = db.relationship('Vendor', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """ Instantiate the User object """
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
