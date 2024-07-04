"""This represents the order model """

from models import db
from models.base_model import BaseModel


class Order(BaseModel):
    """Represents the Order Model """
    __tablename__ = 'orders'
    user_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id'),
        nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    order_items = db.relationship('OrderItem', backref='order', lazy=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
