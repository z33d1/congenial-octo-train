from flask import Flask
from .database import db
from flask_restful import Api
from app.resources.card import Card
from app.resources.auth import Auth
import datetime
import logging
from flask_jwt_extended import JWTManager
from logging.handlers import RotatingFileHandler
from flask_cors import CORS



def create_app(testing_mode=False):
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cards'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['GW-SECRET'] = 'GATEWAY-SECRET'
    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=120)

    if not testing_mode:
        db.init_app(app)

        with app.test_request_context():
            db.create_all()

    api = Api(app)
    api.add_resource(Card, '/card',
                     '/card/<int:card_id>')
    api.add_resource(Auth, '/auth')

    jwt = JWTManager(app)

    handler = logging.handlers.RotatingFileHandler(
        'card.log',
        maxBytes=1024*100,
        backupCount=5)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(filename)s: %(message)s')
    handler.setFormatter(formatter)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    return app