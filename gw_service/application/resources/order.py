from flask_restful import Resource, reqparse, current_app
from application.order_connector import OrderConnector, OrdersNotAvailableException
from application.card_connector import CardConnector
from application.auth_connector import AuthConnector

from application.const import ORDER_SERVICE_ADDRESS as order_addr
from application.const import CARD_SERVICE_ADDRESS as card_addr
from application.const import AUTH_SERVICE_ADDRESS as auth_addr
from flask import request
from celery import Celery, exceptions


celery = Celery('tasks',
                broker='redis://localhost:6379/0')

@celery.task(bind=True)
def silent_create_order(self, user_id, card_id):
    try:
        connector = OrderConnector(order_addr, 'ORDERS')
        _ = connector.create_order_for_user(user_id, card_id)
    except OrdersNotAvailableException:
        print("RETRY:" + str(self.request.retries + 1))
        try:
            self.retry(countdown=10, max_retries=10)
        except exceptions.MaxRetriesExceededError:
            print("Max retries!")

def token_required(func):
    def _check_token(*args, **kwargs):
        auth_headers = request.headers.get('Authorization', '').split()

        if len(auth_headers) != 2:
            return {'message': 'Authorization header required.'}, 401
        if 'Bearer' not in auth_headers:
            return {'message': 'Authorization header format: Bearer `JWT`'}, 401

        a_conn = AuthConnector(auth_addr)

        status, body = a_conn.check_token(auth_headers[1])

        if status == 401:
            return body, status

        return func(*args, **kwargs)
    return _check_token


class Order(Resource):    
    """
    Class to work with Order Resource
    """
    def __init__(self):
        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('card_id', type=int, required=True,
                                      location='json', help="card id is not set")
        super(Order, self).__init__()

    @token_required
    def get(self, user_id,  order_id = None):
        """
        Method to process get responses for server resources
        :param order_id: id of order
        :return: (response data in json, response status code)
        """

        current_app.logger.info("GET: {}".format(request.full_path))

        connector = OrderConnector(order_addr, 'ORDER')
        if order_id is None:
            status, body = connector.get_orders_for_user(user_id)
        else:
            status, body = connector.get_order_by_id(order_id, user_id)

        current_app.logger.debug("Response from servers: {}, {}".format(body,
                                                                        status))
        return body, status

    @token_required
    def delete(self, user_id, order_id = None):
        """
        Method to process DELETE request to Card service
        :param card_id: id of record which need to delete
        :return: (response data in json, response status code)
        """

        current_app.logger.info("DELETE: {}".format(request.full_path))

        o_connector = OrderConnector(order_addr, 'ORDER')
        c_connector = CardConnector(card_addr, 'CARD')        

        if order_id is None:
            _, body_get_id = o_connector.get_orders_for_user(user_id)
            status, body = o_connector.del_all_orders_for_user(user_id)
            if status == 204:              
                for item in body_get_id["orders"]:
                    status_upd, body_upd = c_connector.update_card(item["card_id"], value=-1)
                    if status_upd != 200:
                        return status_upd, body

        else:
            _, body_get_id = o_connector.get_order_by_id(order_id, user_id)
            status, body = o_connector.del_order_by_id(user_id, order_id)
            if status == 204:                            
                card_id = body_get_id["card_id"]
                status_upd, body_upd = c_connector.update_card(card_id, value=-1)
                if status_upd != 200:
                    return body_upd, status_upd

        current_app.logger.debug("Response from cards: {}, {}".format(body,
                                                                        status))
        return body, status
    
    @token_required
    def post(self, user_id):
        """
        Method to process POST request to Order service
        :param user_id: id of user which needed for order
        :return: (response data in json, response status code)
        """
        args = self.post_parser.parse_args()
        card_id = args['card_id']

        current_app.logger.info(f"POST: {request.full_path}")

        o_connector = OrderConnector(order_addr, 'ORDER')
        c_connector = CardConnector(card_addr, 'CARD')

        code, body = c_connector.get_card_by_id(card_id)
               
        if code == 404:
            return {"message":"Can't create order for nonexisting card! Card creating reset."}, 404
        
        status_upd, body_upd = c_connector.update_card(card_id, value=1)

        if status_upd != 200:
            return status_upd, body_upd
        
        try:
            status, body = o_connector.create_order_for_user(user_id, card_id)
        except OrdersNotAvailableException as e:
            res = silent_create_order.delay(user_id, card_id)
            status = 200

        # rollback
        if status != 200:
            status_upd, body_upd = c_connector.update_card(card_id, value=-1)
        
        current_app.logger.debug("Response from card: {}, {}".format(body,
                                                                        status))
        return body, status
