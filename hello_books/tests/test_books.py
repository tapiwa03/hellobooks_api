'''import dependancies'''
import unittest
from flask import json
from hello_books import create_app,db
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from hello_books.models.book_model import Books
from hello_books.models.user_model import User
from hello_books.tests.test_auth import TestAuth




class TestBooks(unittest.TestCase):
    '''Set up methods for test cases'''

    def setUp(self):
        # creates a test client
        self.app = create_app('testing')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
        self.book_data = {
            'book_id': '1',
            'title': 'War and Peace',
            'author': 'Leo Tolstoy',
            'date_published': '02/12/2008',
            'genre': 'fiction',
            'description': 'This is a description about the book war and peace by leo tolstoy',
            'isbn': '1000000000001',
            'copies': '3'
        }
        self.user_data = json.dumps({
            'name': 'Tapiwa',
            'email': 'john@mail.com',
            'password': 'John2018'
        })
        '''register and login a user for test authorization'''
        TestAuth().test_registration
        TestAuth().test_user_login
        
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_book_add(self):
        '''test api can create a book (POST request)'''
        result = self.client.post(
            '/api/v1/books',
            data=json.dumps(
                self.book_data),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)})
        self.assertEqual(result.status_code, 201)
        self.assertIn('Leo Tolstoy', str(result.data))

    def test_book_get_all(self):
        '''test api can get all books stored (GET request)'''
        result = self.client.post(
            '/api/v1/books',
            data=json.dumps(
                self.book_data),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)})
        self.assertEqual(result.status_code, 201)
        result = self.client.get('/api/v1/books')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Leo Tolstoy', str(result.data))

    def test_book_get_by_id(self):
        '''test api can get a single book by its id (GET request)'''
        post_result = self.client.post(
            '/api/v1/books',
            data=json.dumps(
                self.book_data),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)})
        self.assertEqual(post_result.status_code, 201)
        json_result = json.loads(post_result.data.decode())
        result = self.client.get(
            '/api/v1/books/{}'.format(json_result['book_id']),
            content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Leo Tolstoy', str(result.data))

    def test_book_edit(self):
        '''test api can edit a book (PUT request)'''
        self.client.post(
            '/api/v1/books/',
            data=json.dumps(self.book_data),
            content_type='application/json',
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)})
        self.book_data['title'] = 'Newest title'
        response = self.client.put(
            '/api/v1/books/1',
            data=json.dumps(
                self.book_data),
            content_type='application/json', headers={
                'Authorization': 'Bearer {}'.format(self.access_token)})
        self.assertEqual(response.status_code, 200)

    def test_book_delete(self):
        '''test api can delete a single book by id'''
        post_result = self.client.post(
            '/api/v1/books',
            data=json.dumps(self.book_data),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)})
        self.assertEqual(post_result.status_code, 201)
        delete_result = self.client.delete(
            '/api/v1/books/1',
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)})
        self.assertEqual(delete_result.status_code, 200)
        result = self.client.get('/api/v1/books/1')
        self.assertIn(b'Book Doesnt Exist', result.data)



if __name__ == '__main__':
    unittest.main()
