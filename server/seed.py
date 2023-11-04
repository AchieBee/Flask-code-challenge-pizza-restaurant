from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from faker import Faker

from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

fake = Faker()

def seed_data():
    with app.app_context():
        db.create_all()

        # Clear existing data
        Restaurant.query.delete()
        Pizza.query.delete()

        # Populate Restaurants
        for _ in range(25):
            restaurant = Restaurant(
                name=fake.company(),
                address=fake.address(),
                phone_number=fake.phone_number()
            )
            db.session.add(restaurant)

        # Populate Pizzas
        for _ in range(30):
            pizza = Pizza(
                name=fake.word(),
                ingredients=fake.sentence(),
                price=fake.random_int(min=5, max=20)
            )
            db.session.add(pizza)

        db.session.commit()

        # Associate pizzas with restaurants
        restaurants = Restaurant.query.all()
        pizzas = Pizza.query.all()

        for restaurant in restaurants:
            pizzas_to_associate = fake.random_elements(
                elements=pizzas,
                length=fake.random_int(min=1, max=5),
                unique=True
            )

            for pizza in pizzas_to_associate:
                restaurant_pizza = RestaurantPizza(
                    price=fake.random_int(min=5, max=20),
                    restaurant=restaurant,
                    pizza=pizza
                )
                db.session.add(restaurant_pizza)

        db.session.commit()

seed_data()

if __name__ == '__main__':
    app.run()
