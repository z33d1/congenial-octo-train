from flask_restful import Resource, reqparse
from app.models.models import OrderModel
from flask import current_app, request
from app.exceptions import NoOrderException


class Order(Resource):
    def __init__(self):
        self.post_reqparser = reqparse.RequestParser()
        # self.post_reqparser.add_argument('user_id', type=int, required=True,
        #                                  location='json', help="user_id is not set")
        self.post_reqparser.add_argument('card_id', type=int, required=True,
                                         location='json', help="card_id is not set")
    #@jwt_required
    def post(self, user_id):
        """
        Method to process Post request to Rent service
        :return: (response data in json, response status code)
        """
        current_app.logger.info('POST: {}  {}'.format(request.full_path,
                                                     request.get_json(force=True)))
        args = self.post_reqparser.parse_args()

        #todo check card_id exist
        card_id = args['card_id']

        # TODO: may be try..except
        rent_id = OrderModel.create_order(user_id, card_id)

        return {'message': f'order with id: {rent_id} created for {user_id} user_id.'}, 200

    #@jwt_required
    def get(self, user_id=None, order_id=None):
        """
        Method to process get responses for rent resources
        :param user_id:
        :param order_id:
        :return: (response data in json, response status code)
        """

        current_app.logger.info('GET: {}'.format(request.full_path))

        if user_id is None:
            objects = OrderModel.get_all_orders()
            if not objects:
                current_app.logger.warn("Resource not found")
                return {'message': 'orders not found'}, 404
            else:
                return {'orders': [o.to_json() for o in objects]}, 200


        if order_id is None:
            objects = OrderModel.get_orders_for_user(user_id)

            if not objects:
                current_app.logger.warn("Resource not found")
                return {'orders': []}, 200
            else:
                return {'orders': [o.to_json() for o in objects]}, 200

        else:
            order_obj = OrderModel.get_order_for_user_by_id(user_id, order_id)
            if order_obj is None:
                current_app.logger.warn("Resource not found")
                return {'message': 'order not found'}, 404
            else:
                return order_obj.to_json(), 200

    #@jwt_required
    def delete(self, user_id, order_id=None):
        """
        Method to process DELETE request to Rent service
        :param order_id: id of record which need to delete
        :return: (response data in json, response status code)
        """
        current_app.logger.info('DELETE: {}'.format(request.full_path))

        if order_id is None:
            try:
                OrderModel.delete_all_orders(user_id)
            except NoOrderException as e:
                current_app.logger.warn(str(e))
                return {'message': str(e)}, 404
            else:
                return {'message': f'orders for user_id: {user_id} deleted'}, 204


        try:
            OrderModel.delete_order(order_id)
        except NoOrderException as e:
            current_app.logger.warn(str(e))
            return {'message': str(e)}, 404
        else:
            return {'message': f'order with id: {order_id} deleted'}, 204