"""This represents the review model """

from . import db
from .base_model import BaseModel


class Review(BaseModel):
    """Represents the Review model """
    __tablename__ = 'reviews'
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    user_id = db.Column(
        db.String(36),
        db.ForeignKey('users.id'),
        nullable=False)
    vendor_id = db.Column(
        db.String(36),
        db.ForeignKey('vendors.id'),
        nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
