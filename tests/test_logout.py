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

    def test_logout(self):
        '''Test to logout user'''
        #test with correct details
        logout = self.client.post(
            '/api/v1/auth/logout',
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        logout_msg = json.loads(logout.data)
        if re.search("Logged out", str(logout_msg)):
            check = True
        self.assertTrue(check)

     
if __name__ == "__main__":
    unittest.main()
