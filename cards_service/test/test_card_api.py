from app import create_app
from unittest import TestCase
from unittest.mock import patch
from app.models.models import CardModel


class TestCardService(TestCase):

    def setUp(self):

        self.app = create_app(testing_mode=True)
        self.client = self.app.test_client

    def test_bad_request(self):

        res = self.client().get('/card?page=1&size=7')
        self.assertEqual(res.status_code, 400)

    def test_update_attendance_bad_request(self):

        res = self.client().patch('/card/1', json={'value': '3'})
        self.assertEqual(res.status_code, 400)

    @patch('app.models.models.CardModel.attendance_edit')
    def test_update_attendance(self, update_mock):

        update_mock.return_value = None
        res = self.client().patch('/card/1', json={'value': '1'})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'message': 'card with id: 1 attendance updated'})


    @patch('app.models.models.CardModel.get_cards_w_pagination')
    def test_no_cards(self, get_mock):

        get_mock.return_value = None
        res = self.client().get('/card?page=5')

        self.assertEqual(res.status_code, 404)
        self.assertEqual(res.json, {'message': 'cards not found'})

    @patch('app.models.models.CardModel.get_cards_w_pagination')
    def test_get_to_cards(self, get_mock):

        objects = [CardModel(id=1, name="UFC 1", attendance=6),
                    CardModel(id=2, name="UFC 2", attendance=1)]

        get_mock.return_value = objects

        res = self.client().get('/card?page=1&size=2')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'cards': [
                                    {'id': 1, 'Name': "UFC 1",
                                     'Attendance': 6},
                                    {'id': 2, 'Name': "UFC 2",
                                     'Attendance': 1}]})

    @patch('app.models.models.CardModel.get_all_cards')
    def test_get_to_cards_wo_pagination(self, get_mock):

        objects = [CardModel(id=1, name="UFC 1", attendance=6),
                    CardModel(id=2, name="UFC 2", attendance=1)]

        get_mock.return_value = objects

        res = self.client().get('/card?page=0')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'cards': [
                                    {'id': 1, 'Name': "UFC 1",
                                     'Attendance': 6},
                                    {'id': 2, 'Name': "UFC 2",
                                     'Attendance': 1}]})

    @patch('app.models.models.CardModel.get_card')
    def test_get_to_card(self, get_mock):

        object = CardModel(id=1, name="UFC 1", attendance=6)

        get_mock.return_value = object

        res = self.client().get('/card/1')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json, {'card info': {'id': 1, 'Name': "UFC 1",
                                     'Attendance': 6},
                                    })

    @patch('app.models.models.CardModel.del_card')
    def test_del_card(self, delete_mock):

        delete_mock.return_value = None

        res = self.client().delete("/card/1")

        self.assertEqual(res.status_code, 204)

    @patch('app.models.models.CardModel.get_card')
    def test_get_nonexisting_card(self, get_mock):

        get_mock.return_value = None

        res = self.client().get("/card/1")

        self.assertEqual(res.status_code, 404)
    