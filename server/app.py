from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

api = Api(app)

class Welcome(Resource):
    def get(self):
        return {'message': 'Welcome Home'}

# Define the request parser for restaurant data
restaurant_parser = reqparse.RequestParser()
restaurant_parser.add_argument('name', type=str, required=True, help='Name is required')
restaurant_parser.add_argument('address', type=str, required=True, help='Address is required')

# Define the request parser for pizza data
pizza_parser = reqparse.RequestParser()
pizza_parser.add_argument('name', type=str, required=True, help='Name is required')
pizza_parser.add_argument('ingredients', type=str, required=True, help='Ingredients are required')
pizza_parser.add_argument('price', type=float, required=True, help='Price is required')

# Define a resource for listing and creating restaurants
class RestaurantList(Resource):
    @marshal_with({'id': fields.Integer, 'name': fields.String, 'address': fields.String})
    def get(self):
        restaurants = Restaurant.query.all()
        return restaurants

    @marshal_with({'id': fields.Integer, 'name': fields.String, 'address': fields.String})
    def post(self):
        args = restaurant_parser.parse_args()
        restaurant = Restaurant(name=args['name'], address=args['address'])
        db.session.add(restaurant)
        db.session.commit()
        return restaurant, 201

# Define a resource for individual restaurants
class RestaurantResource(Resource):
    @marshal_with({'id': fields.Integer, 'name': fields.String, 'address': fields.String})
    def get(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {'error': 'Restaurant not found'}, 404
        return restaurant

    @marshal_with({'message': fields.String})
    def put(self, id):
        args = restaurant_parser.parse_args()
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {'error': 'Restaurant not found'}, 404
        restaurant.name = args['name']
        restaurant.address = args['address']
        db.session.commit()
        return {'message': 'Restaurant has been updated'}, 200

    @marshal_with({'message': fields.String})
    def delete(self, id):
        restaurant = Restaurant.query.get(id)
        if not restaurant:
            return {'error': 'Restaurant not found'}, 404
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204

# Define a resource for listing and creating pizzas
class PizzaList(Resource):
    @marshal_with({'id': fields.Integer, 'name': fields.String, 'ingredients': fields.String, 'price': fields.Float})
    def get(self):
        pizzas = Pizza.query.all()
        return pizzas

    @marshal_with({'id': fields.Integer, 'name': fields.String, 'ingredients': fields.String, 'price': fields.Float})
    def post(self):
        args = pizza_parser.parse_args()
        pizza = Pizza(name=args['name'], ingredients=args['ingredients'], price=args['price'])
        db.session.add(pizza)
        db.session.commit()
        return pizza, 201

# Add resources to the API
api.add_resource(Welcome, '/')
api.add_resource(RestaurantList, '/restaurants')
api.add_resource(RestaurantResource, '/restaurants/<int:id>')
api.add_resource(PizzaList, '/pizzas')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=5555)
