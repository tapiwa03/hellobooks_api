#test for admin creating another admin, authorize and deauthorize a user
'''importing dependancies'''
import unittest
from flask import json, Flask
from hello_books import create_app, db
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from cerberus import Validator
import datetime
from hello_books.models.book_model import Books
from hello_books.models.user_model import User

app = create_app('testing')
jwt = JWTManager(app)

class TestAuth(unittest.TestCase):
    '''Class for testing user authentication'''


    def setUp(self):
        
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
        self.admin = json.dumps({
            'email': 'tapiwa.lason@gmail.com',
            'password': 'SecretKey1to3'
        })
        self.book_test = json.dumps({
            'book_id': '1',
            'title': 'War and Peace',
            'author': 'Leo Tolstoy',
            'date_published': '02/12/2008',
            'genre': 'fiction',
            'description': 'This is a description about the book war and peace by leo tolstoy',
            'isbn': '1112223334445',
            'copies': '5'
        })
        self.book_add_test = json.dumps({
            'book_id': '2',
            'title': 'War and Peace',
            'author': 'Leo Tolstoy',
            'date_published': '02/12/2008',
            'genre': 'fiction',
            'description': 'This is a description about the book war and peace by leo tolstoy',
            'isbn': '1112223334446',
            'copies': '5'
        })
        self.client.post('/api/v1/auth/register', data=self.user_data)
        login = self.client.post('/api/v1/auth/login', data=self.user_data)
        login_msg = json.loads(login.data)
        self.access_token = login_msg['access_token']
        admin_login = self.client.post('/api/v1/auth/login', data=self.admin)
        login_msg = json.loads(admin_login.data)
        self.admin_access_token = login_msg['access_token']
        

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        
    def test_add_book(self):
        '''Test whether an admin can add a book'''
        result = self.client.post(
            '/api/v1/books',
            data=self.book_test,
            headers={
                    'Authorization': 'Bearer {}'.format(self.admin_access_token)},
            content_type='application/json')
        self.assertEqual(result.status_code, 200)

    def test_make_admin(self):
        '''Test that an admin can change another user to an admin'''
        #test with normal user for error
        result = self.client.put(
            '/api/v1/auth/make-admin',
            data=json.dumps({
                "password": "John2018",
                "email_of_user": "tapiwa.lason@gmail.com"
            }),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(result.status_code, 403)
        #test with admin user
        login = self.client.post('/api/v1/auth/login', data=json.dumps({
            'email': 'tapiwa.lason@gmail.com',
            'password': 'SecretKey1to3'
        }))
        self.assertEqual(login.status_code, 200)
        login_msg = json.loads(login.data)
        access_token = login_msg['access_token']
        result = self.client.put(
            '/api/v1/auth/make-admin',
            data=json.dumps({
                'password': 'SecretKey1to3',
                'email_of_user': 'john@mail.com'
            }),
            headers={
                'Authorization': 'Bearer {}'.format(access_token)},
            content_type='application/json')
        self.assertEqual(result.status_code, 201)
        #test wrong password
        result = self.client.put(
            '/api/v1/auth/make-admin',
            data=json.dumps({
                'password': 'FakePassword',
                'email_of_user': 'john@mail.com'
            }),
            headers={
                'Authorization': 'Bearer {}'.format(access_token)},
            content_type='application/json')
        self.assertEqual(result.status_code, 401)
        #test wrong email
        result = self.client.put(
            '/api/v1/auth/make-admin',
            data=json.dumps({
                'password': 'SecretKey1to3',
                'email_of_user': 'notreal@mail.com'
            }),
            headers={
                'Authorization': 'Bearer {}'.format(access_token)},
            content_type='application/json')
        self.assertEqual(result.status_code, 404)


    def test_authorize_user(self):
        '''Test if an admin can authorize or deauthorize a user'''
        #test with normal user
        result = self.client.put(
            '/api/v1/auth/authorize',
            data=json.dumps({
                'password': 'John2018',
                'email_of_user': 'tapiwa.lason@gmail.com'
            }),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(result.status_code, 403)
        #test with admin
        login = self.client.post('/api/v1/auth/login', data=json.dumps({
            'password': 'SecretKey1to3',
            'email': 'tapiwa.lason@gmail.com'
        }))
        self.assertEqual(login.status_code, 200)
        login_msg = json.loads(login.data)
        access_token = login_msg['access_token']
        auth = self.client.put(
            '/api/v1/auth/authorize',
            data=json.dumps({
                'password': 'SecretKey1to3',
                'email_of_user': 'john@mail.com'
            }),
            headers={
                'Authorization': 'Bearer {}'.format(access_token)},
            content_type='application/json')
        self.assertEqual(auth.status_code, 201)
        #test with wrong password
        auth = self.client.put(
            '/api/v1/auth/authorize',
            data=json.dumps({
                'password': 'False Password',
                'email_of_user': 'john@mail.com'
            }),
            headers={
                'Authorization': 'Bearer {}'.format(access_token)},
            content_type='application/json')
        self.assertEqual(auth.status_code, 401)
        #test with wrong email
        auth = self.client.put(
            '/api/v1/auth/authorize',
            data=json.dumps({
                'password': 'SecretKey1to3',
                'email_of_user': 'john444@mail.com'
            }),
            headers={
                'Authorization': 'Bearer {}'.format(access_token)},
            content_type='application/json')
        self.assertEqual(auth.status_code, 404)


if __name__ == "__main__":
    unittest.main()



