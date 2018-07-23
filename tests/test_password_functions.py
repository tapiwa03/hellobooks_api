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
            'email': 'mapfundetl@gmail.com',
            'password': 'SecretKey1to3'
        })
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

    def test_change_password(self):
        '''Test if user can change password'''
        change = self.client.put(
            '/api/v1/auth/change-password',
            data=json.dumps({
                'new_password': 'Shake321',
                'old_password': 'John2018'     
            }),
            headers={
                    'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(change.status_code, 201)
    
    def test_reset_password(self):
        '''Test if user can reset their password'''
        self.login_user(self.user_data2)
        send = self.client.post(
            '/api/v1/auth/reset-password',
            data=json.dumps({'email': 'mapfundetl@gmail.com'}),
            content_type='application/json'
        )
        self.assertEqual(send.status_code, 200)
    
if __name__ == "__main__":
    unittest.main()
