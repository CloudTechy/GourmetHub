"""This represents the order_item model """

from models import db
from models.base_model import BaseModel


class OrderItem(BaseModel):
    """ Represents the Order Model """
    __tablename__ = 'order_items'
    order_id = db.Column(
        db.String(36),
        db.ForeignKey('orders.id'),
        nullable=False)
    food_item_id = db.Column(
        db.String(36),
        db.ForeignKey('food_items.id'),
        nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    price = db.Column(db.Float, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instantiate the OrderItem Model """
        super().__init__(*args, **kwargs)
