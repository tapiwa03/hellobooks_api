#test for adding, returning, borrowing and deleting a book
"""importing dependancies"""
import re
import unittest
from flask import json, Flask
from hello_books import create_app, db
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)
from cerberus import Validator
import datetime
from hello_books.models.book_model import Books
from hello_books.models.user_model import User

app = create_app('testing')
jwt = JWTManager(app)

class TestAuth(unittest.TestCase):
    """Class for testing user authentication"""


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
            'email': 'tapiwa.lason@gmail.com',
            'password': 'SecretKey1to3'
            }),
            content_type='application/json')
        self.assertEqual(login.status_code, 200)
        login_msg = json.loads(login.data)
        return login_msg['access_token']


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
            'email': 'jane@mail.com',
            'password': 'Jane2018'
        })
        self.wrong_user=json.dumps({
            'email': 'join@mail.com',
            'password': 'John2018'
        })  
        self.admin=json.dumps({
            'email': 'tapiwa.lason@gmail.com',
            'password': 'SecretKey1to3'
        })  
        self.client.post('/api/v1/auth/register', data=self.user_data)    

    def tearDown(self):
        """Runs after every test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login(self):
            '''Test to login user'''
            #test to login
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
            login_msg = json.loads(login.data)
            if re.search("match no record", str(login_msg)):
                check = True
            self.assertTrue(check)
            #test with wrong password
            login = self.client.post('/api/v1/auth/login', data=json.dumps({
                'email': 'tapiwa.lason@gmail.com',
                'password': 'SecretKey787656'
                }),
                content_type='application/json')
            login_msg = json.loads(login.data)
            if re.search("Incorrect Password", str(login_msg)):
                check = True
            self.assertTrue(check)
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
        #register user
        register = self.client.post(
            '/api/v1/auth/register',
            data=self.user_data2)
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
            
           

if __name__ == "__main__":
    unittest.main()



