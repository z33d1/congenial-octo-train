from flask import Flask
from flask_restful import Api
import logging
from .database import db
from app.resources.order import Order
from app.resources.auth import Auth
from logging.handlers import RotatingFileHandler
from datetime import timedelta
from flask_jwt_extended import JWTManager

def create_app(testing_mode=False):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///orders'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['GW-SECRET'] = 'GATEWAY-SECRET'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(seconds=120)

    if not testing_mode:
        db.init_app(app)

        with app.test_request_context():
            db.create_all()

    api = Api(app)
    api.add_resource(Order, '/order','/user/<int:user_id>/order', '/user/<int:user_id>/order/<int:order_id>')
    api.add_resource(Auth, '/auth')
    handler = logging.handlers.RotatingFileHandler(
        'orders.log',
        maxBytes=1024*100,
        backupCount=5)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(filename)s: %(message)s')
    handler.setFormatter(formatter)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    return app
