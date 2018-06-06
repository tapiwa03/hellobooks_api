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
        self.client.post('/api/v1/auth/register', data=self.user_data)
        


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_registration(self):
        '''Test if a user can be registered'''
        result = self.client.post('/api/v1/auth/register', data=self.user_data2)
        self.assertEqual(result.status_code, 201)
        register = json.loads(result.data)
        self.assertEqual(register['message'], "Registered Successfully.")

    def test_user_login(self):
        '''test api allows user to login'''
        result = self.client.post('/api/v1/auth/login', data=json.dumps({
            'email': 'john@mail.com',
            'password': 'John2018'
        }))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'access_token', result.data)

    def test_change_user_password(self):
        '''Test to change a users password'''
        login = self.client.post('/api/v1/auth/login', data=json.dumps({
            'email': 'john@mail.com',
            'password': 'John2018'
        }))
        self.assertEqual(login.status_code, 200)
        login_msg = json.loads(login.data)
        access_token = login_msg['access_token']
        password = {"old_password": "John2018", "new_password": "PasswordNew"}
        change = self.client.put(
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
        reset = self.client.post('/api/v1/auth/reset-password', data=json.dumps({
            'email': 'john@mail.com'
        }),
                              content_type='application/json')
        self.assertEqual(reset.status_code, 201)
        self.assertIn(b'Password has been changed to Pass123', reset.data)

    
    def test_books_not_returned(self):
        '''test to view which books have not been returned by the borrower'''
        login = self.client.post('/api/v1/auth/login', data=json.dumps({
            'email': 'john@mail.com',
            'password': 'John2018'
        }))
        self.assertEqual(login.status_code, 200)
        login_msg = json.loads(login.data)
        access_token = login_msg['access_token']
        check_books = self.client.get(
            '/api/v1/users/books?returned=false',
            headers={
                'Authorization': 'Bearer {}'.format(access_token)},
            content_type='application/json')
        self.assertEqual(check_books.status_code, 200)

    def test_view_users(self):
        '''Test if an admin can view all users'''
        result = self.client.post('/api/v1/auth/login', data=json.dumps({
            'email': 'john@mail.com',
            'password': 'John2018'
        }))
        token = json.loads(result.data)
        access_token = token['access_token']
        view = self.client.get(
            '/api/v1/auth/users',
            headers={
                'Authorization': 'Bearer {}'.format(access_token)},
            content_type='application/json')
        self.assertEqual(view.status_code, 200)

    def test_borrow_history(self):
        '''test to see if a user can retrieve their borrowing history'''
        login = self.client.post('/api/v1/auth/login', data=json.dumps({
            'email': 'john@mail.com',
            'password': 'John2018'
        }))
        self.assertEqual(login.status_code, 200)
        login_msg = json.loads(login.data)
        access_token = login_msg['access_token']
        history = self.client.get(
            '/api/v1/users/books',
            headers={
                'Authorization': 'Bearer {}'.format(access_token)},
            content_type='application/json')
        self.assertEqual(history.status_code, 200)

    def test_user_logout(self):
        '''test api allows user to logout'''
        result = self.client.post('/api/v1/auth/login', data=json.dumps({
            'email': 'john@mail.com',
            'password': 'John2018'
        }))
        token = json.loads(result.data)
        access_token = token['access_token']
        res = self.client.post(
            'api/v1/auth/logout',
            headers={
                'Authorization': 'Bearer {}'.format(access_token)},
            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"You are now logged out", res.data)


if __name__ == "__main__":
    unittest.main()


    """def test_return_book(self):
        '''test to return a borrowed books'''
        result = self.client.post(
            '/api/v1/auth/register', data=self.user_data2)
        self.assertEqual(result.status_code, 201)
        login = self.client.post('/api/v1/auth/login', data=json.dumps({
            'email': 'jane@mail.com',
            'password': 'Jane2018'
        }))
        self.assertEqual(login.status_code, 200)
        login_msg = json.loads(login.data)
        access_token = login_msg['access_token']
        return_book = self.client.put(
            '/api/v1/users/books/1',
            headers={
                'Authorization': 'Bearer {}'.format(access_token)},
            content_type='application/json')
        self.assertEqual(return_book.status_code, 201)

    def test_borrow_book(self):
        '''test to borrow a book'''
        login = self.client.post('/api/v1/auth/login', data=json.dumps({
            'email': 'john@mail.com',
            'password': 'John2018'
        }))
        login_msg = json.loads(login.data)
        access_token = login_msg['access_token']
        due_date = {"due_date": "07/07/2027"}
        borrow = self.client.post(
            '/api/v1/users/books/1',
            data=json.dumps(due_date),
            headers={
                'Authorization': 'Bearer {}'.format(access_token)},
            content_type='application/json')
        self.assertEqual(borrow.status_code, 201)
    

    def test_make_admin(self):
        '''Test that an admin can change another user to an admin'''
        login = self.client.post('/api/v1/auth/login', data=json.dumps({
            'email': 'jane@mail.com',
            'password': 'Jane2018'
        }))
        self.assertEqual(login.status_code, 200)
        login_msg = json.loads(login.data)
        access_token = login_msg['access_token']
        result = self.client.put(
            '/api/v1/auth/make-admin',
            data=json.dumps({
                'password': 'John2018',
                'email': 'jane@mail.com'
            }),
            headers={
                'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(result.status_code, 201)

    def test_authorize_user(self):
        '''Test if an admin can authorize or deauthorize a user'''
        login = self.client.post('/api/v1/auth/login', data=json.dumps({
            'email': 'jane@mail.com',
            'password': 'Jane2018'
        }))
        self.assertEqual(login.status_code, 200)
        login_msg = json.loads(login.data)
        access_token = login_msg['access_token']
        auth = self.client.put(
            '/api/v1/auth/authorize',
            data=json.dumps({
                'password': 'John2018',
                'email': 'jane@mail.com'
            }),
            headers={
                'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(auth.status_code, 201)
    """

