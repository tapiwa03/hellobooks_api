#test for admin creating another admin, authorize and deauthorize a user
'''importing dependancies'''
import unittest
from flask import json, Flask
from api import create_app, db

app = create_app('testing')


class TestAuth(unittest.TestCase):
    '''Test adding book'''


    def setUp(self):
        
        # creates a test client
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
        self.admin = json.dumps({
            'name': 'Taps',
            'email': 'tapiwa.lason@yandex.com',
            'password': 'SecretKey1to3'
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
        #register admin
        self.client.post('/api/v1/auth/register', data=self.admin)
        self.admin_access_token = self.login_admin()
        self.add_book()
        
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login_admin(self):
        """Login the admin"""
        log = self.client.post('/api/v1/auth/login', data=json.dumps({
            'email': 'tapiwa.lason@yandex.com',
            'password': 'SecretKey1to3'
            }),
            content_type='application/json')
        self.assertEqual(log.status_code, 200)
        login_adm = json.loads(log.data)
        return login_adm['access_token']

    def add_book(self):
        '''create a book'''
        add = self.client.post(
            '/api/v1/books',
            data=self.book_test,
            headers={
                    'Authorization': 'Bearer {}'.format(self.admin_access_token)},
            content_type='application/json')
        self.assertEqual(add.status_code, 201)
        
    def test_get_all_books(self):
        '''Test to Retrieve all the books'''
        get = self.client.get(
            '/api/v1/books',
            headers={
                    'Authorization': 'Bearer {}'.format(self.admin_access_token)})
        self.assertEqual(get.status_code, 200)

    def test_get_book_by_id(self):
        '''Test if user can get book by id'''
        get = self.client.get(
            '/api/v1/books/1',
            headers={
                    'Authorization': 'Bearer {}'.format(self.admin_access_token)})
        self.assertEqual(get.status_code, 200)

if __name__ == "__main__":
    unittest.main()



