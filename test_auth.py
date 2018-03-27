from hello_books import app
import unittest 
import json

class TestAuth(unittest.TestCase): 
    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True 
        #Initialize test variables
        self.user_data = {
            'email': 'john@mail.com',
            'password': 'John2018'
        }
        


    def test_registration(self):
        # sends HTTP GET request to the application
        # on the specified path
        result = self.app.post('/api/v1/auth/register') 

        # assert the status code of the response
        self.assertEqual(result.status_code, 201)
        #assert that registration message shows
        self.assertEqual(result.json(), {'message':'Registered Successfully'}) 

    def test_user_login(self):
        #test api allows user to login
        self.test_registration()
        result=self.client().post('/api/v1/auth/login', data=dict(
            email='john@mail.com',
            password='John2018'
            ))
        self.assertIn(b'You are now logged in', result.data)


    def test_user_logout(self):
        #test api allows user to logout
        #register and login first
        self.test_user_login()
        #follow redirect to logout and message displayed
        res = self.client().get('api/v1/auth/logout', follow_redirects=True)
        self.assertIn(b'You were logged out', res.data)



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

    def tearDown(self):
        #Teardown Initialized variables
        pass




if __name__ == "__main__":
    unittest.main()