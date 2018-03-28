from hello_books import app, jwt
from flask import Flask, json, jsonify

#Import unittest and os dependancy module
import unittest


class TestBooks(unittest.TestCase):
    #Set up methods for test cases
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 
        self.book_data = json.dumps({
            'book_id':'1',
            'title':'War and Peace',
            'author': 'Leo Tolstoy',
            'date_published': '02/12/2008',
            'genre':'fiction',
            'description':'This is a description about the book war and peace by leo tolstoy'
        })


    def test_book_add(self):
        #test api can create a book (POST request)
        result = self.app.post('/api/v1/books', data=self.book_data)
        self.assertEqual(result.status_code, 201)
        self.assertIn('Book Added', str(result.data))


    def test_book_get_all(self):
        #test api can get all books stored (GET request)
        result = self.app.post('/api/v1/books', data=self.book_data)
        self.assertEqual(result.status_code, 201)
        result = self.app.get('/api/v1/books')
        self.assertEqual(result.status_code, 200)
        self.assertIn('Leo Tolstoy', str(result.data))


    def test_book_get_by_id(self):
        #test api can get a single book by its id (GET request)
        post_result = self.app.post('/api/v1/books', data=self.book_data)
        self.assertEqual(post_result.status_code, 201)
        json_result = json.loads(post_result.decode('utf-8').replace("'","\""))
        result = self.app.get(
            '/api/v1/books/{}'.format(json_result['book_id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Leo Tolstoy', str(result.data))


    def test_book_edit(self):
        #test api can edit a book (PUT request)
        post_result = self.app.post('/api/v1/books', data=self.book_data)
        self.assertEqual(post_result.status_code, 201)
        post_result = self.app.put(
            'api/v1/books/1',
            data=json.dumps({
                "author": "No more author"
            }))
        self.assertEqual(post_result.status_code,200)
        result = self.app.get('/api/v1/books/1')
        self.assertIn('No more author', str(result.data))


    def test_book_delete(self):
        #test api can delete a single book by id
        post_result = self.app.post('/api/v1/books', data=self.book_data)
        self.assertEqual(post_result.status_code, 201)
        delete_result = self.app.delete('/api/v1/books/1')
        self.assertEqual(delete_result.status_code, 200)
        result = self.app.get('/api/v1/books/1')
        self.assertEqual(result.status_code, 404)


    def tearDown(self):
        #Teardown Initialized variables
        pass

if __name__ == '__main__':
    unittest.main()
