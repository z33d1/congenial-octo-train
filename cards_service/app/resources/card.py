from flask_restful import Resource, reqparse
from app.models.models import CardModel
from flask import current_app, request
from app.exceptions import NoCardException


class Card(Resource):
    def __init__(self):
        self.get_reqparser = reqparse.RequestParser()
        self.get_reqparser.add_argument('page', type=int, required=False, default=0,
                                   help='No pagination page')
        self.get_reqparser.add_argument('size', type=int, choices=[1, 2, 3, 4, 5],
                                   default=5, help='Incorrect size per page')

        self.put_reqparser = reqparse.RequestParser()
        self.put_reqparser.add_argument('delta', type=int, required=True,
                                     choices=[1, -1], location='json',
                                     help="delta is not set or incorrect")

        self.patch_reqparser = reqparse.RequestParser()
        self.patch_reqparser.add_argument('value', type=int, required=True,
                                     choices=[1, -1], location='json',
                                     help="value is not set or incorrect")

                            

        super(Card, self).__init__()

    #@jwt_required
    def get(self, card_id=None):
        """
        Method to process get responses for card resources
        :param card_id: id of card
        :return: (response data in json, response status code)
        """

        current_app.logger.info('GET: {}'.format(request.full_path))

        if card_id is None:
            args = self.get_reqparser.parse_args()
            page = args['page']
            per_page = args['size']

            if page == 0:
                objects = CardModel.get_all_cards()
            else:
                objects = CardModel.get_cards_w_pagination(page, per_page)

            if not objects:
                current_app.logger.warn("Resource not found")
                return {'message': 'cards not found'}, 404
            else:
                return {'cards': [o.to_json() for o in objects]}, 200

        else:
            res = CardModel.get_card(card_id)
            if res is None:
                current_app.logger.warn("Resource not found")
                return {'message': 'card not found'}, 404
            else:
                # resp_body = res[0].to_json()
                # resp_body.update(res[1].to_json())
                return {'card info': res.to_json()}, 200

    def delete(self, card_id):
        """
        Method to process DELETE request to Card service
        :param card_id: id of record which need to delete
        :return: (response data in json, response status code)
        """
        current_app.logger.info('DELETE: {}'.format(request.full_path))

        try:
            CardModel.del_card(card_id)
        except NoCardException as e:
            current_app.logger.warn(str(e))
            return {'message': str(e)}, 404
        else:
            return {'message': 'card with id: {} deleted'.format(card_id)}, 204

    def patch(self, card_id):
        """
        Method to process UPDATE request to Card service
        :param card_id: id of record which need to delete
        :param value: 1 - to increase attendance, -1 - decrease attendance
        :return: (response data in json, response status code)
        """
        current_app.logger.info('PATCH: {}'.format(request.full_path))
        args = self.patch_reqparser.parse_args()
        value = args["value"]

        try:
            CardModel.attendance_edit(card_id, value)
        except NoCardException as e:
            current_app.logger.warn(str(e))
            return {'message': str(e)}, 404
        else:
            return {'message': 'card with id: {} attendance updated'.format(card_id)}, 200



    # #@jwt_required
    # def put(self, card_id):
    #     """
    #     Method to process put responses for card resources
    #     :param card_id: id of card
    #     :return: (response data in json, response status code)
    #     """

    #     current_app.logger.info('PUT: {}'.format(request.full_path))
    #     args = self.put_reqparser.parse_args()

    #     try:
    #         updated_count = ServerInfoModel.update_card_available(card_id,
    #                                                             args['delta'])
    #     except NoServerException as e:
    #         current_app.logger.warn(str(e))
    #         return {'message': str(e)}, 404
    #     else:
    #         return {'available count': updated_count}, 200