"""This represents the food_item model """

from . import db
from .base_model import BaseModel


class FoodItem(BaseModel):
    """represents the Food_Items Model """
    __tablename__ = 'food_items'
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    vendor_id = db.Column(
        db.String(36),
        db.ForeignKey('vendors.id'),
        nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    orders = db.relationship('OrderItem', backref='food_item', lazy=True)

    def __init__(self, *args, **kwargs):
        """ Instantiate the foodItem object """
        super().__init__(*args, **kwargs)
