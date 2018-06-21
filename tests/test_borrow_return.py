#test for adding, returning, borrowing and deleting a book
"""importing dependancies"""
import unittest
from flask import json
from api import create_app, db

app = create_app('testing')

class TestAuth(unittest.TestCase):
    """Testing Borrow and return functions"""

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
        self.add_books(self.book_test)
        self.login_user(user= self.user)

    def tearDown(self):
        """Runs after every test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login_user(self, user):
        """Log in a user"""
        login = self.client.post(
            '/api/v1/auth/login',
            data=self.user,
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
        '''Borrow a book'''
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
        #Test with non existent book ID
        borrow = self.client.post(
            '/api/v1/users/books/121322',
            data=json.dumps(due_date),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)},
            content_type='application/json')
        self.assertEqual(borrow.status_code, 404)

if __name__ == "__main__":
    unittest.main()



