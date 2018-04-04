'''importing dependancies'''
import unittest
from flask import json, Flask
from hello_books import app, jwt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from cerberus import Validator



class TestAuth(unittest.TestCase):
    '''Class for testing user authentication'''


    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        # Initialize test variables
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
        self.book_test = {
            'book_id': '1',
            'title': 'War and Peace',
            'author': 'Leo Tolstoy',
            'date_published': '02/12/2008',
            'genre': 'fiction',
            'description': 'This is a description about the book war and peace by leo tolstoy'
        }

    def test_registration(self):
        '''sends HTTP GET request to the application'''
        result = self.app.post('/api/v1/auth/register', data=self.user_data)
        # assert the status code of the response
        self.assertEqual(result.status_code, 201)
        # assert that registration message shows
        self.assertIn(
            result.data,
            b'{\n  "message": "Registered Successfully"\n}\n')

    def test_user_login(self):
        '''test api allows user to login'''
        result = self.app.post('/api/v1/auth/login', data=json.dumps({
            'email': 'john@mail.com',
            'password': 'John2018'
        }))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'access_token', result.data)

    def test_user_logout(self):
        '''test api allows user to logout'''
        result = self.app.post('/api/v1/auth/login', data=json.dumps({
            'email': 'john@mail.com',
            'password': 'John2018'
        }))
        token = json.loads(result.data)
        access_token = token['access_token']
        res = self.app.post(
            'api/v1/auth/logout',
            headers={
                'Authorization': 'Bearer {}'.format(access_token)},
            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"You are now logged out", res.data)

    def test_change_user_password(self):
        '''Test to register new user'''
        result = self.app.post('/api/v1/auth/register', data=self.user_data2)
        self.assertEqual(result.status_code, 200)
        # login the registered user
        login = self.app.post('/api/v1/auth/login', data=json.dumps({
            'email': 'jane@mail.com',
            'password': 'Jane2018'
        }))
        self.assertEqual(login.status_code, 200)
        login_msg = json.loads(login.data)
        access_token = login_msg['access_token']
        password = {"old_password": "Jane2018", "new_password": "PasswordNew"}
        change = self.app.put(
            '/api/v1/auth/change-password',
            data=json.dumps(password),
            headers={
                'Authorization': 'Bearer {}'.format(access_token)},
            content_type='application/json')
        self.assertEqual(change.status_code, 201)
        change_msg = json.loads(change.data)
        self.assertEqual(change_msg['message'], 'Password has been changed')

    def test_reset_password(self):
        '''reset the password'''
        reset = self.app.post('/api/v1/auth/reset-password', data=json.dumps({
            'email': 'jane@mail.com'
        }),
                              content_type='application/json')
        self.assertEqual(reset.status_code, 201)
        self.assertIn(b'Password has been changed to Pass123', reset.data)

    def test_borrow_book(self):
        '''test to borrow a book'''
        result = self.app.post('/api/v1/auth/register', data=self.user_data2)
        self.assertEqual(result.status_code, 201)
        login = self.app.post('/api/v1/auth/login', data=json.dumps({
            'email': 'jane@mail.com',
            'password': 'Jane2018'
        }))
        self.assertEqual(login.status_code, 200)
        login_msg = json.loads(login.data)
        access_token = login_msg['access_token']
        result = self.app.post(
            '/api/v1/books', data=json.dumps(self.book_test))
        self.assertEqual(result.status_code, 201)
        due_date = {"due_date": "07/07/2027"}
        borrow = self.app.post(
            '/api/v1/users/books/1',
            data=json.dumps(due_date),
            headers={
                'Authorization': 'Bearer {}'.format(access_token)},
            content_type='application/json')
        self.assertEqual(borrow.status_code, 201)

    def tearDown(self):
        # Teardown Initialized variables
        pass


if __name__ == "__main__":
    unittest.main()
