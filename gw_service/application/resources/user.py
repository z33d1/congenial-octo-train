from flask_restful import Resource, reqparse, current_app
from application.user_connector import UserConnector
from application.const import USER_SERVICE_ADDRESS as addr
from flask import request


class User(Resource):
    """
    Class to work with User Resource
    """
    def __init__(self):
        super(User, self).__init__()

    def get(self, user_id=None):

        current_app.logger.info("GET: {}".format(request.full_path))

        connector = UserConnector(addr, 'USER')

        if user_id == None:
            status, body = connector.get_users()
        else:
            status, body = connector.get_user_by_id(user_id)

        current_app.logger.debug("Response from servers: {}, {}".format(body,
                                                                        status))
        return body, status