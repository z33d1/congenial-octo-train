from flask_restful import Resource, reqparse, current_app
from application.card_connector import CardConnector
from application.order_connector import OrderConnector
from application.user_connector import UserConnector

from application.const import CARD_SERVICE_ADDRESS as card_addr
from application.const import ORDER_SERVICE_ADDRESS as order_addr
from application.const import USER_SERVICE_ADDRESS as user_addr
from flask import request


class CardUser(Resource):
    """
    Class to work with CardUser Resource
    """
    def __init__(self):
        super(CardUser, self).__init__()

    def get(self, card_id):
        """
        Method to get all user for exact card
        :param server_id: id of server
        :return: (response data in json, response status code)
        """

        current_app.logger.info("GET: {}".format(request.full_path))

        card_connector = CardConnector(card_addr, 'CARD')
        order_connector = OrderConnector(order_addr, 'ORDER')
        user_connector = UserConnector(user_addr, 'USER')

        code_order, body_order = order_connector.get_orders()

        user_list = []
        body_list = []

        for order in body_order["orders"]:
            if card_id == order["card_id"]:
                user_list.append(order["user_id"])

        body = {}

        user_connector.get_users()
        
        for user in user_list:
            status, body = user_connector.get_user_by_id(user)
            # degradation
            if status == 503:
                body.update({'user_info': {'id': user, 'username': 'some username'}})         
            print(body)       
            body_list.append(body)
            
        return {"users_for_this_card": body_list}, 200

