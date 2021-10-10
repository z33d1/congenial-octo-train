from .service_connector import ServiceConnector
from flask_restful import current_app

class OrdersNotAvailableException(Exception):
    pass

class OrderConnector(ServiceConnector):
    """
    Class to connect with Orders Service
    """
    # def get_servers_with_pag(self, page, size):
    #     """
    #     Method to get info about servers using pagination
    #     :param page: page number
    #     :param size: count elements per page
    #     :return: (response code, response data in json)
    #     """

    #     url = "/server?page={}&size={}".format(page, size)
    #     return self.send_get_request(url, with_token=True)

    def get_orders(self):
        """
        Method to get info about all orders
        :return: (response code, response data in json)
        """

        url = f"/order"
        code, body = self.send_get_request(url)
        current_app.logger.debug("Response from order: {}, {}".format(body, code))
        return code, body

    def get_orders_for_user(self, user_id):
        """
        Method to get info about all orders for user
        :return: (response code, response data in json)
        """

        url = f"/user/{user_id}/order"
        code, body = self.send_get_request(url)
        current_app.logger.debug("Response from order: {}, {}".format(body, code))
        return code, body

    def get_order_by_id(self, order_id, user_id):
        """
        Method to get info about server with server_id
        :param server_id: id of server which need to get
        :return: (response code, response data in json)
        """

        url = f"/user/{user_id}/order/{order_id}"
        code, body = self.send_get_request(url)
        current_app.logger.debug("Response from order: {}, {}".format(body, code))
        
        return code, body

    def del_order_by_id(self, user_id, order_id):
        """
        Method to delete info about order with order_id
        :param order_id: id of order which need to get
        :return: (response code, response data in json)
        """
        url = f"/user/{user_id}/order/{order_id}"
        return self.send_delete_request(url)

    def del_all_orders_for_user(self, user_id):
        """
        Method to delete all orders for user with user_id
        :param user_id: id of user which orders need to del
        :return: (response code, response data in json)
        """
        url = f"/user/{user_id}/order"
        return self.send_delete_request(url)

    def create_order_for_user(self, user_id, card_id):
        """
        Method to create order with order_id
        :param order_id: id of order which need to get
        :return: (response code, response data in json)
        """
        url = f"/user/{user_id}/order"
        code, body = self.send_post_request(url, {'card_id': card_id})
        current_app.logger.debug("Response from order: {}, {}".format(body, code))
        if code == 503:
            raise OrdersNotAvailableException
        return code, body
