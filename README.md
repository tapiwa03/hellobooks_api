[![Build Status](https://travis-ci.org/3V0L/bootcamp-c2.svg?branch=master)](https://travis-ci.org/3V0L/bootcamp-c2)
[![Coverage Status](https://coveralls.io/repos/github/3V0L/bootcamp-c2/badge.svg?branch=master)](https://coveralls.io/github/3V0L/bootcamp-c2?branch=master)

# Hellobooks 

Hellobooks is a library management API. A list of the functions available in the system is shown below.

## API Functionality

|Endpoint                  | Functionality              |HTTP method 
|--------------------------|----------------------------|-------------
|/api/books                |Add a book                  |POST        
|/api/books/*book_id*       |modify a book’s information |PUT
|/api/books/*book_id*      |Remove a book               |DELETE
|/api/books                |Retrieves all books         |GET
|/api/books/*book_id*       |Get a book                  |GET
|/api/users/books/*book_id* |Borrow a book               |POST
|/api/auth/register        |Creates a user account      |POST
|/api/auth/login           |Logs in a user              |POST
|/api/auth/logout          |Logs out a user             |POST
|/api/auth/reset-password  |Password reset              |POST
|/api/auth/change-password  |Change password              |POST

## How to run this application

 - Clone this repository
 - Set up a virtual environment
 - Install the apps dependencies by running `pip install -r requirements.txt`
 - Open the terminal in the app's main directory
 - Run `python run.py`

 
## How to run this application
- The app makes use of JWT tokens for authentication and can take JSON requests at will.
- Postman is used to input data and get output data from the system
- PyTest is used to test the endpoints of the APIs
- First register a user with a name, email and password. After that login. Then it is possible to change password, and borrow a book under a normal user
- For the book functions you need to enter the book data in the following JSON format otherwise it will raise an error:
```
{
    'book_id':'1',
    'title':'War and Peace',
    'author': 'Leo Tolstoy',
    'date_published': '02/12/2008',
    'genre':'fiction',
    'description':'This is a description about the book war and peace by leo tolstoy'
}
```
- User data is also entered in json format and should take the same format as above


## Made by 3V0L