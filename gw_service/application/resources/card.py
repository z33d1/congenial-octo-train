from flask_restful import Resource, reqparse, current_app
from application.card_connector import CardConnector, CardsNotAvailableException
from application.order_connector import OrderConnector
from application.const import CARD_SERVICE_ADDRESS as addr
from application.const import ORDER_SERVICE_ADDRESS as order_addr
from flask import request

from circuitbreaker import circuit


class Card(Resource):
    """
    Class to work with Card Resource
    """
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('page', type=int, required=False, default=0,
                                   help='No pagination page')
        self.reqparse.add_argument('size', type=int, choices=[1, 2, 3, 4, 5],
                                   default=5, help='Incorrect size per page')
        super(Card, self).__init__()

    @circuit(failure_threshold=5, expected_exception=CardsNotAvailableException, recovery_timeout=100)
    def get(self, card_id=None):
        """
        Method to process get responses for server resources
        :param server_id: id of server
        :return: (response data in json, response status code)
        """

        current_app.logger.info("GET: {}".format(request.full_path))

        connector = CardConnector(addr, 'CARD')
        if card_id is None:
            args = self.reqparse.parse_args()
            page, size = args['page'], args['size']

            if page == 0:
                status, body = connector.get_cards()
            else:
                status, body = connector.get_cards_w_pagination(page, size)
        else:
            status, body = connector.get_card_by_id(card_id)

        current_app.logger.debug("Response from cards: {}, {}".format(body,
                                                                        status))
        return body, status

    def delete(self, card_id):
        """
        Method to process DELETE request to Card service
        :param card_id: id of record which need to delete
        :return: (response data in json, response status code)
        """
        #TODO when delete card with it deleting orders on this card
        current_app.logger.info("GET: {}".format(request.full_path))

        connector = CardConnector(addr, 'CARD')
        order_connector = OrderConnector(order_addr, 'ORDER')

        status, body = connector.del_card_by_id(card_id)
        status_order, body_order = order_connector.get_orders()

        if status_order == 404:
            current_app.logger.debug("Response from servers: {}, {}".format(body_order,
                                                                        status_order))
            return body_order, status_order
        else:
            for order in body_order["orders"]:
                if order["card_id"] == card_id:
                    status_order, body_order = order_connector.del_order_by_id(order["user_id"], order["id"])
                    if status_order != 204:
                        current_app.logger.debug("Response from servers: {}, {}".format(body_order,
                                                                        status_order))
                        return body, status
            
            

        current_app.logger.debug("Response from servers: {}, {}".format(body,
                                                                        status))
        return body, status