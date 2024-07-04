""" This is the base modekl for all models in the gourmetHub app """

from datetime import datetime
from uuid import uuid4 as uuid
from models import db

time = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel(db.Model):
    """ This is the base model for all models in the gourmetHub app """
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=str(uuid()))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.now,
        onupdate=datetime.now)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid())

    def save(self):
        """ Save the model to the database """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """ Delete the model from the database """
        db.session.delete(self)
        db.session.commit()

    def update(self, **kwargs):
        """ Update the model in the database """
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()
    
    def to_dict(self):
        """ Return a dictionary representation of the model """
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns if c.name != "password"}

    @classmethod
    def find_by_id(cls, id):
        """ Find a model by its id """
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        """ Find all models of this type """
        return cls.query.all()

    @classmethod
    def find_by(cls, **kwargs):
        """ Find a model by a given attribute """
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def find_all_by(cls, **kwargs):
        """ Find all models by a given attribute """
        return cls.query.filter_by(**kwargs).all()

    def __repr__(self):
        """ Return a string representation of the model """
        return f'<{self.__class__.__name__} {self.id}>'
