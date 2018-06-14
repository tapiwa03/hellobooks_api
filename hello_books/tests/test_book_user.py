#test for adding, returning, borrowing and deleting a book
"""importing dependancies"""
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
            'email': 'jane@mail.com',
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
        self.book_test2 = {
            'book_id': '2',
            'title': 'War and Peace',
            'author': 'Leo Tolstoy',
            'date_published': '02/12/2008',
            'genre': 'fiction',
            'description': 'This is a description about the book war and peace by leo tolstoy',
            'isbn': '1112223334446',
            'copies': '5'
        }  
        self.user=json.dumps({
            'email': 'john@mail.com',
            'password': 'John2018'
        })   
        self.client.post('/api/v1/auth/register', data=self.user_data)


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
            'email': 'tapiwa.lason@gmail.com',
            'password': 'SecretKey1to3'
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
        self.assertEqual(result.status_code, 200)


    def borrow_book(self):
        due_date = {"due_date": "07/07/2018"}
        borrow = self.client.post(
            '/api/v1/users/books/1',
            data=json.dumps(due_date),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(borrow.status_code, 201)    


    def test_return_book(self):
        """test to return a borrowed book"""
        self.add_books(book=self.book_test)
        self.login_user(user=self.user)
        self.borrow_book()
        #test with wrong user
        return_book = self.client.put(
            '/api/v1/users/books/1',
            headers={
                'Authorization': 'Bearer {}'.format(self.admin_access_token)},
            content_type='application/json')
        self.assertEqual(return_book.status_code, 401)
        #test with correct user
        return_book = self.client.put(
            '/api/v1/users/books/1',
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(return_book.status_code, 201)
        #return the same book again
        return_book = self.client.put(
            '/api/v1/users/books/1',
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(return_book.status_code, 401)
        #test with nonexistent book
        return_book = self.client.put(
            '/api/v1/users/books/1234',
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(return_book.status_code, 404)
        

    def test_borrow_book(self):
        """test to borrow a book"""
        self.add_books(book=self.book_test)
        self.login_user(user= self.user)
        due_date = {"due_date": "07/07/2018"}
        borrow = self.client.post(
            '/api/v1/users/books/1',
            data=json.dumps(due_date),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(borrow.status_code, 201)
        #Test with wrong date
        due_date = {"due_date": "07/07/2020"}
        borrow = self.client.post(
            '/api/v1/users/books/1',
            data=json.dumps(due_date),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(borrow.status_code, 401)
        #wrong format date
        due_date = {"due_date": "07/07-2020"}
        borrow = self.client.post(
            '/api/v1/users/books/1',
            data=json.dumps(due_date),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(borrow.status_code, 401)
        #Test with non existent book ID
        borrow = self.client.post(
            '/api/v1/users/books/121322',
            data=json.dumps(due_date),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(borrow.status_code, 404)

    def test_boooks_not_returned(self):
        """Test if a users borrowing history for books not returned"""
        self.add_books(book=self.book_test)
        self.login_user(user= self.user)
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
        #test after returning book  
        return_book = self.client.put(
            '/api/v1/users/books/1',
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(return_book.status_code, 201)
        not_returned = self.client.get(
            '/api/v1/users/books?returned=false',
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(not_returned.status_code, 200) 

    def test_borrowing_history(self):
        """Test if admin can view a users borrowing history"""
        self.add_books(book=self.book_test)
        self.login_user(user= self.user)
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



