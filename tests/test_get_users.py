#test for adding, returning, borrowing and deleting a book
"""importing dependancies"""
import re
import unittest
from flask import json, Flask
from api import create_app, db
app = create_app('testing')

class TestAuth(unittest.TestCase):
    """Class for testing user login and register"""


    def setUp(self):
        """Runs before every test"""
        # creates a test client
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
        self.user_data = json.dumps({
            'name': 'Tapiwa',
            'email': 'john@mail.com',
            'password': 'John2018'
        })
        self.user_data2 = json.dumps({
            'name': 'Password',
            'email': 'tapiwa.lason@yandex.com',
            'password': 'SecretKey1to3'
        })
        self.wrong_user = json.dumps({
            'email': 'join@mail.com',
            'password': 'John2018'
        })
        self.admin = json.dumps({
            'email': 'tapiwa.lason@yandex.com',
            'password': 'SecretKey1to3'
        })
        self.client.post('/api/v1/auth/register', data=self.user_data2)
        self.login_user(self.user_data)

    def tearDown(self):
        """Runs after every test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login_user(self, user):
        """Create a user and log them in"""
        self.client.post('/api/v1/auth/register', data=user)
        #login  user
        login = self.client.post(
            '/api/v1/auth/login',
            data=json.dumps({
                'email': 'john@mail.com',
                'password': 'John2018'     
            }),
            content_type='application/json')
        login_msg = json.loads(login.data)
        self.access_token = login_msg['access_token']

    def login_admin(self):
        """Login the admin"""
        login = self.client.post('/api/v1/auth/login', data=json.dumps({
            'email': 'tapiwa.lason@yandex.com',
            'password': 'SecretKey1to3'
            }),
            content_type='application/json')
        self.assertEqual(login.status_code, 200)
        login_msg = json.loads(login.data)
        return login_msg['access_token']

    def test_get_all_users(self):
        '''Test if admin can get all users'''
        token = self.login_admin()
        get_all = self.client.get(
            '/api/v1/auth/users?page=1&results=2',
            headers={
                    'Authorization': 'Bearer {}'.format(token)})
        self.assertEqual(get_all.status_code, 200)

    def test_authorize_user(self):
        '''Test if admin can authorize a user'''
        token = self.login_admin()
        auth = self.client.put(
            '/api/v1/auth/authorize',
            data=json.dumps({
                "email_of_user": "john@mail.com",
                "password": "SecretKey1to3"
            }),
            headers={
                'Authorization': 'Bearer {}'.format(token)},
            content_type='application/json')
        self.assertEqual(auth.status_code, 201)
        #test deauthorize user
        auth = self.client.put(
            '/api/v1/auth/authorize',
            data=json.dumps({
                "email_of_user": "john@mail.com",
                "password": "SecretKey1to3"
            }),
            headers={
                'Authorization': 'Bearer {}'.format(token)},
            content_type='application/json')
        self.assertEqual(auth.status_code, 201)

if __name__ == "__main__":
    unittest.main()
