from flask_restful import Resource, reqparse
from app.models.models import UserModel
from flask import current_app, request
# from flask_jwt_extended import jwt_required


class User(Resource):
    def __init__(self):
        self.put_parser = reqparse.RequestParser()
        super(User, self).__init__()


    def get(self, user_id=None):
        """
        Method to process get responses for user resources
        :param user_id: id of user
        :return: (response data in json, response status code)
        """

        current_app.logger.info("GET: {}".format(request.full_path))
        
        if user_id == None:
            res = UserModel.get_users()
            if res is None:
                current_app.logger.warn("Resource not found")
                return {'message': 'users not found'}, 404
            else:
                return {'users': [o.to_json() for o in res]}, 200

        else:
            res = UserModel.get_user_info_by_id(user_id)
            if res is None:
                current_app.logger.warn("Resource not found")
                return {'message': 'user not found'}, 404
            else:
                resp_body = res.to_json()
                return {'user_info': resp_body}, 200

class HelloWorld(Resource):
    def get(self):
        return {'msg': "HELOO"}, 200