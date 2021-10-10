from application import create_app
from unittest import TestCase
from unittest.mock import patch


class TestServerResource(TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client

    def test_bad_get_user(self):
        res = self.client().get("/users")
        self.assertEqual(res.status_code, 404)

    @patch('application.user_connector.UserConnector.get_user_by_id')
    def test_get_user(self, mock):
        mock.return_value = (200,
        {
            "user info": {
                "id": 1,
                "name": "Kizilov D."
            }
        })
        res = self.client().get("/user/1")
        self.assertEqual(res.status_code, 200)
        