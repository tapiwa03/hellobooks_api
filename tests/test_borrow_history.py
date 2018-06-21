#test for adding, returning, borrowing and deleting a book
"""importing dependancies"""
import unittest
from flask import json, Flask
from api import create_app, db
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, get_raw_jwt
)
from api.models.validate import HelloBooks
from api.models.book import Books
from api.models.user import User
from api.models.borrow import Borrow
import datetime


app = create_app('testing')
jwt = JWTManager(app)

class TestAuth(unittest.TestCase):
    """Class for testing user book borrowing"""


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
            'email': 'jane@yandex.com',
            'password': 'Jane2018'
        })
        self.book_test = json.dumps({
            "book_id": '1',
            "title": "War and Peace",
            "author": "Leo Tolstoy",
            "date_published": "02/12/2008",
            "genre": "fiction",
            "description": "This is a description about the book war and peace by leo tolstoy",
            "isbn": "1112223334445",
            "copies": "5"
        })
        self.user=json.dumps({
            'email': 'john@mail.com',
            'password': 'John2018'
        })   
        self.client.post('/api/v1/auth/register', data=self.user_data)
        self.client.post('/api/v1/auth/register', data=self.user_data2)
        self.add_books(book=self.book_test)
        self.login_user(user= self.user)


    def tearDown(self):
        """Runs after every test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


    def login_user(self, user):
        """Log in a user"""
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
            'email': 'jane@yandex.com',
            'password': 'Jane2018'
            }),
            content_type='application/json')
        self.assertEqual(login.status_code, 200)
        login_msg = json.loads(login.data)
        return login_msg['access_token']

    def add_books(self, book):
        self.admin_access_token = self.login_admin()
        result = self.client.post(
            '/api/v1/books',
            data=book,
            headers={
                    'Authorization': 'Bearer {}'.format(self.admin_access_token)},
            content_type='application/json')
        self.assertEqual(result.status_code, 201)


    def borrow_book(self):
        due_date = {"due_date": "07/07/2018"}
        borrow = self.client.post(
            '/api/v1/users/books/1',
            data=json.dumps(due_date),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(borrow.status_code, 201)    

    def test_boooks_not_returned(self):
        """Test if a users borrowing history for books not returned"""
        #test without borrowing a book
        not_returned = self.client.get(
            '/api/v1/users/books?returned=false',
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(not_returned.status_code, 200)     
        #test after borrowing a book  
        self.borrow_book()
        not_returned = self.client.get(
            '/api/v1/users/books?returned=false',
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(not_returned.status_code, 200)   

    def test_borrowing_history(self):
        """Test if admin can view a users borrowing history"""
        history = self.client.get(
            '/api/v1/users/books',
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(history.status_code, 404)
        self.borrow_book()
        history = self.client.get(
            '/api/v1/users/books',
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(history.status_code, 200)

if __name__ == "__main__":
    unittest.main()
