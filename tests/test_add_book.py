#test for admin creating another admin, authorize and deauthorize a user
'''importing dependancies'''
import unittest
from flask import json
from api import create_app, db

app = create_app('testing')


class TestAuth(unittest.TestCase):
    '''Test adding book'''


    def setUp(self):
        '''Runs before every test'''
        # creates a test client
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
        self.user_data = json.dumps({
            'name': 'Tapiwa',
            'email': 'jane@mail.com',
            'password': 'John2018'
        })
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
        #register normal user
        self.client.post('/api/v1/auth/register', data=self.user_data)
        login = self.client.post('/api/v1/auth/login', data=json.dumps({
            'email': 'jane@mail.com',
            'password': 'John2018'
        }))
        login_msg = json.loads(login.data)
        self.access_token = login_msg['access_token']
        #register admin
        self.client.post('/api/v1/auth/register', data=self.admin)
        self.admin_access_token = self.login_admin()
        
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

    def test_add_book(self):
        '''Test whether an admin can create a book'''
        add = self.client.post(
            '/api/v1/books',
            data=self.book_test,
            headers={
                'Authorization': 'Bearer {}'.format(self.admin_access_token)},
            content_type='application/json')
        self.assertEqual(add.status_code, 201)
        #add book again
        add = self.client.post(
            '/api/v1/books',
            data=self.book_test,
            headers={
                'Authorization': 'Bearer {}'.format(self.admin_access_token)},
            content_type='application/json')
        self.assertEqual(add.status_code, 409)

    def test_delete_book(self):
        '''Test whether admin can delete a book'''
        add = self.client.post(
            '/api/v1/books',
            data=self.book_test,
            headers={
                'Authorization': 'Bearer {}'.format(self.admin_access_token)},
            content_type='application/json')
        self.assertEqual(add.status_code, 201)
        #delete book
        delete = self.client.delete(
            '/api/v1/books/1',
            headers={
                'Authorization': 'Bearer {}'.format(self.admin_access_token)})
        self.assertEqual(delete.status_code, 200)

if __name__ == "__main__":
    unittest.main()
