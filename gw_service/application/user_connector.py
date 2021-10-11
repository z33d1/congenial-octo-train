from .service_connector import ServiceConnector
from flask_restful import current_app

class UsersNotAvailableException(Exception):
    pass


class UserConnector(ServiceConnector):
    """
    Class to connect with Users Service
    """
    def get_user_by_id(self, user_id):
        """
        Method to get info about user with user_id
        :param user_id: id of user which need to get
        :return: (response code, response data in json)
        """
        url = f"/user/{user_id}"
        return self.send_get_request(url)

    def get_users(self):
        """
        Method to get users
        :return: (response code, response data in json)
        """
        url = f"/user"

        code, body = self.send_get_request(url)
        
        current_app.logger.debug("Response from user connector: {}, {}".format(body, code))
        
        return code, body