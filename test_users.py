#Import unittest and os dependancy module
import unittest
import os

# import JSON
from flask import json
import json

from app import create_app


class UsersTestsCase(unittest.TestCase):
    #Set up methods for test cases
    def setUp(self):
    	#Initialize test variables
        self.app = create_app("testing")
        self.client = self.app.test_client
        self.user_data = {
    	   	'email': 'john@mail.com',
    	   	'password': 'John2018'
    	}
        self.app_context = self.app.app_context()
        self.app_context.push()


    def test_user_registration(self):
    	#Test api can register user
    	result = self.client().post('/api/auth/register', data=self.user_data)
    	self.assertEqual(result.status_code, 201)


    def test_user_login(self):
    	#test api allows user to login
    	self.test_user_registration()
    	result=self.client().post('/auth/login', data=dict(
    		email='john@mail.com',
    		password='John2018'
    		), follow_redirects=True)
    	self.assertIn(b'You are now logged in', result.data)


    def test_user_logout(self):
    	#test api allows user to logout
    	#register and login first
    	self.test_user_login
    	#follow redirect to logout and message displayed
    	res = self.client().get('/auth/logout', follow_redirects=True)
    	self.assertIn(b'You were logged out', res.data)



    def test_user_password_reset(self):
    	#test api allows user to reset their password /api/auth/reset-password
    	self.test_user_login()
    	reset_result = self.client().post('/auth/reset-password', data={
    		'email':'john@mail.com',
    		'old_password':'John2018',
    		'new_password':'Change123'
    	})
    	login_result = self.client().post('/auth/login', data={
    		'email':'john@mail.com',
    		'password':'Change123'
    	})
    	self.assertEqual(login_result.status_code, 200)


    def tearDown(self):
    	#Teardown Initialized variables
    	self.app_context.pop()




if __name__ == '__main__':
    unittest.main()




