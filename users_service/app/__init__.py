from flask import Flask
from flask_restful import Api
import logging
from .database import db
from app.resources.user import User, HelloWorld
# from application.resources.auth import Auth
from logging.handlers import RotatingFileHandler
from datetime import timedelta
# from flask_jwt_extended import JWTManager


def create_app(testing_mode=False):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    if not testing_mode:
        db.init_app(app)

        with app.test_request_context():
            db.create_all()

    api = Api(app)
    api.add_resource(User, '/user', '/user/<int:user_id>')
    api.add_resource(HelloWorld, '/')
    # api.add_resource(Auth, '/auth')

    # jwt = JWTManager(app)

    handler = logging.handlers.RotatingFileHandler(
        'users.log',
        maxBytes=1024*100,
        backupCount=5)

    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(filename)s: %(message)s')
    handler.setFormatter(formatter)
    app.logger.setLevel(logging.DEBUG)
    app.logger.addHandler(handler)

    return app
