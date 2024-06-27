"""This represents the vendor model """

from models import db
from models.base_model import BaseModel


class Vendor(BaseModel):
    __tablename__ = 'vendors'
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id'),
        nullable=False)
    food_items = db.relationship('FoodItem', backref='vendor', lazy=True)
    # user = db.relationship('User', backref='vendors', lazy=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
