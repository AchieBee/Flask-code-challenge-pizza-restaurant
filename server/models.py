from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import validates

db = SQLAlchemy()

#SerializerMixin
class SerializerMixin:
    @property
    def serialize(self):
        return {key: getattr(self, key) for key in self.__mapper__.c.keys()}

# Restaurant model
class Restaurant(db.Model, SerializerMixin):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='restaurant', cascade='all, delete-orphan')
    phone_number = db.Column(db.String(20))

    # Rules for validation
    @validates('name')
    def validate_name(self, key, value):
        if len(value.strip()) == 0:
            raise ValueError('Name cannot be empty')
        return value

    @validates('address')
    def validate_address(self, key, value):
        if len(value.strip()) == 0:
            raise ValueError('Address cannot be empty')
        return value



# Pizza model
class Pizza(db.Model, SerializerMixin):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    restaurant_pizzas = db.relationship('RestaurantPizza', backref='pizza', cascade='all, delete-orphan')
    price = db.Column(db.Float)

    # Rules for validation 
    @validates('name')
    def validate_name(self, key, value):
        if len(value.strip()) == 0:
            raise ValueError('Name cannot be empty')
        return value


# RestaurantPizza model
class RestaurantPizza(db.Model, SerializerMixin):
    __tablename__ = 'restaurant_pizzas'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)


