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

    def test_login(self):
        '''Test to login user'''
        #test with correct details
        login = self.client.post(
            '/api/v1/auth/login',
            data=self.admin,
            content_type='application/json')
        login_msg = json.loads(login.data)
        if re.search("access_token", str(login_msg)):
            check = True
        self.assertTrue(check)
        #test with wrong credentials
        login = self.client.post(
            '/api/v1/auth/login',
            data=self.wrong_user,
            content_type='application/json')
        self.assertEqual(login.status_code, 404)
        #test with wrong password
        login = self.client.post('/api/v1/auth/login', data=json.dumps({
            'email': 'tapiwa.lason@gmail.com',
            'password': 'SecretKey787656'
            }),
            content_type='application/json')
        self.assertEqual(login.status_code, 404)
        #test with no email
        login = self.client.post('/api/v1/auth/login', data=json.dumps({
            'password': 'Secr6hg56'
            }),
            content_type='application/json')
        login_msg = json.loads(login.data)
        if re.search("input email", str(login_msg)):
            check = True
        self.assertTrue(check)

    def test_register_user(self):
        '''Test to register a user'''
        #test with correct details
        register = self.client.post(
            '/api/v1/auth/register',
            data=self.user_data)
        register_msg = json.loads(register.data)
        if re.search("Registered", str(register_msg)):
            check = True
        self.assertTrue(check)
        #register user again
        register = self.client.post(
            '/api/v1/auth/register',
            data=self.user_data2,
            content_type='application/json')
        register_msg = json.loads(register.data)
        if re.search("Exists", str(register_msg)):
            check = True
        self.assertTrue(check)
        #register incorrect data format
        register = self.client.post(
            '/api/v1/auth/register',
            data=self.wrong_user,
            content_type='application/json')
        register_msg = json.loads(register.data)
        if re.search("Please input", str(register_msg)):
            check = True
        self.assertTrue(check)
        #register with no data
        register = self.client.post(
            '/api/v1/auth/register',
            data=json.dumps({}),
            content_type='application/json')
        self.assertEqual(register.status_code, 400)

if __name__ == "__main__":
    unittest.main()
