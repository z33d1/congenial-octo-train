from flask import Flask
from flask_restful import Api
from .database import db
from application.resources.auth import UserLogin, TokenRefresh, TokenCheck
from application.resources.auth import AppToken, AppCode
from flask_cors import CORS


def create_app(testing_mode=False):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    app.config['JWT_ACCESS_SECRET'] = 'jwt-access-secret'
    app.config['JWT_REFRESH_SECRET'] = 'jwt-refresh-secret'

    app.config['APPS'] = {'1': ['SECRET_KEY_APP_1', ''],
                          '2': ['SECRET_KEY_APP_2', '']}

    cors = CORS(app, resources={r"*": {"origins": "*"}})

    if not testing_mode:
        db.init_app(app)

        with app.test_request_context():
            db.create_all()

    api = Api(app)
    api.add_resource(UserLogin, '/auth/login')
    api.add_resource(TokenRefresh, '/auth/refresh')
    api.add_resource(TokenCheck, '/auth/check')
    api.add_resource(AppCode, '/auth/code')
    api.add_resource(AppToken, '/auth/token')

    return app

