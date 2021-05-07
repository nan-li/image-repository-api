from server import app # get from a level up if put in /tests
from unittest import TestCase
from model import connect_to_db, db, example_data
from flask import session
import json

class BaseTestCase(TestCase):

    def setUp(self):
        """Setup before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()


    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

def register_user(self, username, password):
    return self.client.post(
        '/users/register',
        data=json.dumps(dict(
            username=username,
            password=password
        )),
        content_type='application/json',
    )

class TestSomething(BaseTestCase):
    def test_registration(self):
        """Test for user registration."""
        with self.client:
            response = register_user(self, 'testuser', 'testpassword')
            data = json.loads(response.data.decode())

            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Account successfully created.')
            self.assertTrue(data['username'] == 'testuser')
            self.assertTrue(data['user_id'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    import unittest

    unittest.main()