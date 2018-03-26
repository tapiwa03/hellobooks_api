#Import unittest and os dependancy module
import unittest
import os

# import JSON
import json

from app import create_app



class BooksTestsCase(unittest.TestCase):
    #Set up methods for test cases
    def setUp(self):
    	#Initialize test variables
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.book_data = {
    	   	'book_id':'1',
    	   	'title':'War and Peace',
    	   	'author': 'Leo Tolstoy',
    	   	'date_published': '02/12/2008',
    	   	'genre':'fiction',
    	   	'description':'This is a description about the book war and peace by leo tolstoy'
    	}
        self.app_context = self.app.app_context()
        self.app_context.push()



    def test_book_add(self):
    	#test api can create a book (POST request)
    	result = self.client().post('/api/books', data=self.book_data)
    	self.assertEqual(result.status_code, 201)
    	self.assertIn('Leo Tolstoy', str(result.data))


    def test_book_get_all(self):
    	#test api can get all books stored (GET request)
    	result = self.client().post('/api/books', data=self.book_data)
    	self.assertEqual(result.status_code, 201)
    	result = self.client().get('/api/books')
    	self.assertEqual(result.status_code, 200)
    	self.assertIn('Leo Tolstoy', str(result.data))


    def test_book_get_by_id(self):
    	#test api can get a single book by its id (GET request)
    	post_result = self.client().post('/api/books', data=self.book_data)
    	self.assertEqual(post_result.status_code, 201)
    	json_result = json.loads(post_result.decode('utf-8').replace("'","\""))
    	result = self.client().get(
    		'/api/books/{}'.format(json_result['book_id']))
    	self.assertEqual(result.status_code, 200)
    	self.assertIn('Leo Tolstoy', str(result.data))


    def test_book_edit(self):
    	#test api can edit a book (PUT request)
    	post_result = self.client().post('/api/books', data=self.book_data)
    	self.assertEqual(post_result.status_code, 201)
    	post_result = self.client().put(
    		'api/books/1',
    		data={
    		    "author": "No more author"
    		})
    	self.assertEqual(post_result.status_code,200)
    	result = slef.client().get('/api/books/1')
    	self.assertIn('No more author', str(result.data))


    def test_book_delete(self):
    	#test api can delete a single book by id
    	post_result = self.client().post('/api/books', data=self.book_data)
    	self.assertEqual(post_result.status_code, 201)
    	delete_result = self.client().list_of_books.remove('/api/books/1')
    	self.assertEqual(delete_result.status_code, 200)
    	result = self.client().get('/api/books/1')
    	self.assertEqual(result.status_code, 404)


    def tearDown(self):
        #Teardown Initialized variables
    	self.app_context.pop()


if __name__ == '__main__':
    unittest.main()



