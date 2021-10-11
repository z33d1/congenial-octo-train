from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from application.resources.card import Card
from application.resources.user import User
from application.resources.order import Order
from application.resources.card_user import CardUser

import logging
from logging.handlers import RotatingFileHandler


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['GW-SECRET'] = ''
    app.config['CARD'] = ''
    app.config['USERS'] = ''
    app.config['ORDER'] = ''

    cors = CORS(app, resources={r"*": {"origins": "*"}})

    api = Api(app)
    api.add_resource(CardUser, '/card/<int:card_id>/user')
    api.add_resource(Card, '/card',
                     '/card/<int:card_id>')
    api.add_resource(User, '/user', '/user/<int:user_id>')
    api.add_resource(Order, '/order','/user/<int:user_id>/order',
      '/user/<int:user_id>/order/<int:order_id>')


    handler = logging.handlers.RotatingFileHandler(
        'gateway.log',
        maxBytes=1024*100,
        backupCount=5)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(filename)s: %(message)s')
    handler.setFormatter(formatter)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    return app