from .service_connector import ServiceConnector
from flask_restful import current_app


class CardsNotAvailableException(Exception):
    pass

class CardConnector(ServiceConnector):
    """
    Class to connect with Servers Service
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

    def get_cards(self):
        """
        Method to get info about all servers
        :return: (response code, response data in json)
        """
        url = "/card"
        code, body = self.send_get_request(url)
        if code == 503:
            raise CardsNotAvailableException
        return code, body

    def get_card_by_id(self, card_id):
        """
        Method to get info about server with server_id
        :param server_id: id of server which need to get
        :return: (response code, response data in json)
        """
        url = f"/card/{card_id}"
        return self.send_get_request(url)

    def get_cards_w_pagination(self, page, size):
        """
        Method to get info about server with server_id
        :param server_id: id of server which need to get
        :return: (response code, response data in json)
        """
        url = f"/card?page={page}&size={size}"
        return self.send_get_request(url)

    def del_card_by_id(self, card_id):
        """
        Method to delete info about server with server_id
        :param server_id: id of server which need to get
        :return: (response code, response data in json)
        """
        url = f"/card/{card_id}"
        return self.send_delete_request(url)

    def update_card(self, card_id, value):
        """
        Method to delete info about server with server_id
        :param server_id: id of server which need to get
        :return: (response code, response data in json)
        """
        url = f"/card/{card_id}"
        code, body = self.send_patch_request(url, {'value': value})
        if code == 503:
            raise CardsNotAvailableException
    
        current_app.logger.debug("Response from order: {}, {}".format(body, code))
        return code, body