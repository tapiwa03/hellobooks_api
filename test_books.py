import os, sys
#from hello_books import app, jwt
from flask import Flask, json, jsonify
from cerberus import Validator

#Import unittest and os dependancy module
import unittest
from hello_books import app, jwt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from cerberus import Validator



# Import the view file

class TestBooks(unittest.TestCase):
    #Set up methods for test cases
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 
        self.book_data = {
            'book_id':'1',
            'title':'War and Peace',
            'author': 'Leo Tolstoy',
            'date_published': '02/12/2008',
            'genre':'fiction',
            'description':'This is a description about the book war and peace by leo tolstoy'
        }


    def test_book_add(self):
        #test api can create a book (POST request)
        result = self.app.post('/api/v1/books', data=json.dumps(self.book_data))
        self.assertEqual(result.status_code, 201)
        self.assertIn('Leo Tolstoy', str(result.data))


    def test_book_get_all(self):
        #test api can get all books stored (GET request)
        result = self.app.post('/api/v1/books', data=json.dumps(self.book_data))
        self.assertEqual(result.status_code, 201)
        result = self.app.get('/api/v1/books')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Leo Tolstoy', str(result.data))


    
    def test_book_get_by_id(self):
        #test api can get a single book by its id (GET request)
        post_result = self.app.post('/api/v1/books', data=json.dumps(self.book_data))
        self.assertEqual(post_result.status_code, 201)
        json_result = json.loads(post_result.data.decode())
        result = self.app.get(
            '/api/v1/books/{}'.format(json_result['book_id']), content_type='application/json')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Leo Tolstoy', str(result.data))
    
    

    def test_book_edit(self):
        #test api can edit a book (PUT request)
        self.app.post('/api/v1/books/', data=json.dumps(self.book_data),
                         content_type='application/json')
        self.book_data['title'] = 'Newest title'
        response = self.app.put('/api/v1/books/1', data=json.dumps(self.book_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)


    def test_book_delete(self):
        #test api can delete a single book by id
        post_result = self.app.post(
            '/api/v1/books', data=json.dumps(self.book_data))
        self.assertEqual(post_result.status_code, 201)
        delete_result = self.app.delete('/api/v1/books/1')
        self.assertEqual(delete_result.status_code, 200)
        result = self.app.get('/api/v1/books/1')
        self.assertIn(b'Book Doesnt Exist', result.data)


    def tearDown(self):
        #Teardown Initialized variables
        pass

if __name__ == '__main__':
    unittest.main()
