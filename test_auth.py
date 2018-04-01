from hello_books import app, jwt
import unittest 
from flask import Flask, json, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from cerberus import Validator


class TestAuth(unittest.TestCase): 
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 
        #Initialize test variables
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


    def test_registration(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.post('/api/v1/auth/register', data=self.user_data) 

        # assert the status code of the response
        self.assertEqual(result.status_code, 201)
        #assert that registration message shows
        self.assertIn(result.data,  b'{\n  "message": "Registered Successfully"\n}\n')


    def test_user_login(self):
        #test api allows user to login
        result=self.app.post('/api/v1/auth/login', data=json.dumps({
            'email' : 'john@mail.com',
            'password' : 'John2018'
            }))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'access_token', result.data)

    def test_user_logout(self):
        #test api allows user to logout
        result=self.app.post('/api/v1/auth/login', data=json.dumps({
            'email' : 'john@mail.com',
            'password' : 'John2018'
            }))
        #follow redirect to logout and message displayed
        token = json.loads(result.data)
        access_token = token['access_token']
        res = self.app.delete('api/v1/auth/logout',
                            headers={'Authorization': 'Bearer {}'.format(access_token)},
                            content_type='application/json')
        self.assertEqual(res.status_code , 200)
        self.assertIn(b"You are now logged out", res.data)


    def test_change_user_password(self):
        #Test to register new user
        result = self.app.post('/api/v1/auth/register', data=self.user_data2)
        # assert the status code of the response
        self.assertEqual(result.status_code, 201)
        #login the registered user
        login = self.app.post('/api/v1/auth/login', data=json.dumps({
            'email': 'jane@mail.com',
            'password': 'Jane2018'
        }))
        self.assertEqual(login.status_code, 200)
        #retrieve data from the login response
        login_msg = json.loads(login.data)
        access_token = login_msg['access_token']
        #set variable for the new password
        new_password = {"new_pword": "PasswordNew"}
        #do a post of the new password to see if it changes
        change = self.app.post('/api/v1/auth/change-password',
                                data=json.dumps(new_password),
                                headers={'Authorization': 'Bearer {}'.format(access_token)},
                                content_type='application/json')
        self.assertEqual(change.status_code, 201)
        change_msg = json.loads(change.data)
        self.assertEqual(change_msg['message'], 'Password has been changed')


    def test_reset_password(self):
        #reset the password
        reset = self.app.post('/api/v1/auth/reset-password', data=json.dumps({
                                'email' : 'jane@mail.com'
                                }),
                              content_type='application/json')
        self.assertEqual(reset.status_code, 201)
        self.assertIn(b'Password has been changed to Pass123', reset.data)
  

    def tearDown(self):
        #Teardown Initialized variables
        pass




if __name__ == "__main__":
    unittest.main()  

