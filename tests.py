from server import app # get from a level up if put in /tests
from unittest import TestCase
from model import User, Image, connect_to_db, db
from flask import session
import json
from werkzeug.security import generate_password_hash

def example_data():
    """Create some sample data for testing."""

    # In case this is run more than once, empty out existing data
    User.query.delete()
    Image.query.delete()

    # Add sample users and images
    user1 = User(username='user1', password_hash=generate_password_hash('test1'))
    user2 = User(username='user2', password_hash=generate_password_hash('test2'))

    user1image1 = Image(image_url='url/for/user1image1', owner=user1)
    user2image1 = Image(image_url='url/for/user2image1', owner=user2)
    user1image2_public = Image(image_url='url/for/user1image2_private', 
                                owner=user1, permission='PUBLIC')

    db.session.add_all([user1, 
                        user2, 
                        user1image1, 
                        user2image1, 
                        user1image2_public])
    db.session.commit()


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

class TestRegistration(BaseTestCase):
    def test_successful_registration(self):
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

    
    def test_registration_with_already_used_username(self):
        """Test registration with already registered username."""
        with self.client:
            response = register_user(self, 'user1', 'testpassword')
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Username already exists.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    import unittest

    unittest.main()