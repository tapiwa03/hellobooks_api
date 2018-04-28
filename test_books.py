'''import dependancies'''
import unittest
from flask import json
from hello_books import app


class TestBooks(unittest.TestCase):
    '''Set up methods for test cases'''

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        self.app.testing = True
        self.book_data = {
            'book_id': '1',
            'title': 'War and Peace',
            'author': 'Leo Tolstoy',
            'date_published': '02/12/2008',
            'genre': 'fiction',
            'description': 'This is a description about the book war and peace by leo tolstoy'
            'isbn': '1000000000001',
            'copies': '3'
        }
        self.user_data = json.dumps({
            'name': 'Tapiwa',
            'email': 'john@mail.com',
            'password': 'John2018'
        })
        '''register and login a user for test authorization'''
        result = self.app.post('/api/v1/auth/register', data=self.user_data)
        result = self.app.post('/api/v1/auth/login', data=json.dumps({
            'email': 'john@mail.com',
            'password': 'John2018'
        }))
        token = json.loads(result.data)
        self.access_token = token['access_token']

    def test_book_add(self):
        '''test api can create a book (POST request)'''
        result = self.app.post(
            '/api/v1/books',
            data=json.dumps(
                self.book_data),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)})
        self.assertEqual(result.status_code, 201)
        self.assertIn('Leo Tolstoy', str(result.data))

    def test_book_get_all(self):
        '''test api can get all books stored (GET request)'''
        result = self.app.post(
            '/api/v1/books',
            data=json.dumps(
                self.book_data),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)})
        self.assertEqual(result.status_code, 201)
        result = self.app.get('/api/v1/books')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Leo Tolstoy', str(result.data))

    def test_book_get_by_id(self):
        '''test api can get a single book by its id (GET request)'''
        post_result = self.app.post(
            '/api/v1/books',
            data=json.dumps(
                self.book_data),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)})
        self.assertEqual(post_result.status_code, 201)
        json_result = json.loads(post_result.data.decode())
        result = self.app.get(
            '/api/v1/books/{}'.format(json_result['book_id']),
            content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Leo Tolstoy', str(result.data))

    def test_book_edit(self):
        '''test api can edit a book (PUT request)'''
        self.app.post(
            '/api/v1/books/',
            data=json.dumps(self.book_data),
            content_type='application/json',
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)})
        self.book_data['title'] = 'Newest title'
        response = self.app.put(
            '/api/v1/books/1',
            data=json.dumps(
                self.book_data),
            content_type='application/json', headers={
                'Authorization': 'Bearer {}'.format(self.access_token)})
        self.assertEqual(response.status_code, 200)

    def test_book_delete(self):
        '''test api can delete a single book by id'''
        post_result = self.app.post(
            '/api/v1/books',
            data=json.dumps(self.book_data),
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)})
        self.assertEqual(post_result.status_code, 201)
        delete_result = self.app.delete(
            '/api/v1/books/1',
            headers={
                'Authorization': 'Bearer {}'.format(self.access_token)})
        self.assertEqual(delete_result.status_code, 200)
        result = self.app.get('/api/v1/books/1')
        self.assertIn(b'Book Doesnt Exist', result.data)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
