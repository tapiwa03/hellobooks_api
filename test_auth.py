from hello_books import app, jwt
import unittest 
from flask import Flask, json, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from hello_books.api.auth_views import register

class TestAuth(unittest.TestCase): 
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        #self.jwt = JWTManager(app)
        # propagate the exceptions to the test client
        self.app.testing = True 
        #Initialize test variables
        self.user_data = json.dumps({
            'name': 'Tapiwa',
            'email': 'john@mail.com',
            'password': 'John2018'
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
        self.test_registration()
        result=self.app.post('/api/v1/auth/login', data=json.dumps({
            'email' : 'john@mail.com',
            'password' : 'John2018'
            }))
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'access_token', result.data)

    def test_user_logout(self):
        #test api allows user to logout
        #register and login first
        self.test_registration()
        result=self.app.post('/api/v1/auth/login', data=json.dumps({
            'email' : 'john@mail.com',
            'password' : 'John2018'
            }))
        #follow redirect to logout and message displayed
        token = json.loads(result.data)
        access_token = token['access_token']
        res = self.app.post('api/v1/auth/logout',
                            headers={'Authorization': 'Bearer {}'.format(access_token)})
        self.assertEqual(res.data , 200)
        self.assertIn(b"You are now logged out", res.data)


    def tearDown(self):
        #Teardown Initialized variables
        pass




if __name__ == "__main__":
    unittest.main()  
   

""""
    



        registration = self.register_user(self.user)
        self.assertEqual(registration.status_code, 201)
        login = self.login_user(self.user)
        self.assertEqual(login.status_code, 200)
        login_msg = json.loads(login.data)
        access_token = login_msg['access_token']
        logout = self.client.post('/api/auth/logout',
                                  headers={'Authorization': 'Bearer {}'.format(access_token)})
        logout_msg = json.loads(logout.data)
        self.assertEqual(logout.status_code, 200)
        self.assertEqual(logout_msg['message'], 'successfully logged out')



    def test_user_password_reset(self):
        #test api allows user to reset their password /api/auth/reset-password
        self.test_user_login()
        reset_result = self.client().post('api/v1/auth/reset-password', data={
            'email':'john@mail.com',
            'old_password':'John2018',
            'new_password':'Change123'
        })
        login_result = self.client().post('/auth/login', data={
            'email':'john@mail.com',
            'password':'Change123'
        })
        self.assertEqual(login_result.status_code, 200)
"""

