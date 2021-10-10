from application import create_app
from unittest import TestCase
from unittest.mock import patch


class TestServerResource(TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

    def test_bad_pagination(self):
        res = self.client().get('/card?page=1&size=6')
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json, {"message":
                                    {"size": "Incorrect size per page"}})

    @patch('application.card_connector.CardConnector.get_cards_w_pagination')
    def test_pagination(self, mock):
        mock.return_value = (200, {'cards': [{'id': 1, 'Name': "UFC 1",'Attendance': 6} ]} )
        res = self.client().get('/card?page=1&size=1')
        self.assertEqual(res.status_code, 200)

    @patch('application.card_connector.CardConnector.get_card_by_id')
    def test_get_server_by_id(self, mock):
        mock.return_value = (200, {'cards': [{'id': 1, 'Name': "UFC 1",'Attendance': 6} ]} )

        res = self.client().get('/card/1')

        self.assertEqual(res.status_code, 200)

    @patch('application.card_connector.CardConnector.get_cards')
    def test_get_cards(self, mock):
        mock.return_value = (200, {'cards': [
                                    {'id': 1, 'Name': "UFC 1",
                                     'Attendance': 6},
                                    {'id': 2, 'Name': "UFC 2",
                                     'Attendance': 1}]})

        res = self.client().get('/card')                                     

        self.assertEqual(res.status_code, 200)


    @patch('application.card_connector.CardConnector.del_card_by_id')
    def test_del_card_by_id(self, mock):
        
        mock.return_value = (204, {'cards': [
                                    {'id': 1, 'Name': "UFC 1",
                                     'Attendance': 6},
                                    {'id': 2, 'Name': "UFC 2",
                                     'Attendance': 1}]})

        res = self.client().delete('/card/1')                                     

        self.assertEqual(res.status_code, 500)


        
