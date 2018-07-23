[![Build Status](https://travis-ci.org/3V0L/hellobooks_api.svg?branch=ft-real-data-api-156137706)](https://travis-ci.org/3V0L/hellobooks_api)  [![Coverage Status](https://coveralls.io/repos/github/3V0L/hellobooks_api/badge.svg?branch=ft-real-data-api-156137706)](https://coveralls.io/github/3V0L/hellobooks_api?branch=ft-real-data-api-156137706)  [![Maintainability](https://api.codeclimate.com/v1/badges/1c662ee03a51b905706d/maintainability)](https://codeclimate.com/github/3V0L/hellobooks_api/maintainability)

# Hellobooks 

Hellobooks is a small library management API. It allows users to borrow and return books with a limit of 5 books being avaiilable to them at a time. 

Administrators are the only ones who can add, delete and edit books. Admins are registered through the use of a yandex mail email available [here](https://mail.yandex.com). If a different type of email is required it can be changed within the users model of the api. 

There is a time limit imposed on the weeks a user can borrow a book for, the time is 2 months. 

Any suggestions for improvements are greatly appreciated. 

## Hosted
The documentation is hosted on [apiary](https://hellobooks8.docs.apiary.io/)
The API itself is available on [heroku](https://hellobooks-tapiwa.herokuapp.com/)

## API Functionality

|Endpoint                  | Functionality              |HTTP method 
|--------------------------|----------------------------|-------------
|/api/books                |Add a book (Admin Only)                  |POST        
|/api/books/*book_id*       |modify a book’s information (Admin Only) |PUT
|/api/books/*book_id*      |Remove a book (Admin Only)               |DELETE
|/api/books                |Retrieves all books         |GET
|/api/books/*book_id*       |Get a book by id                  |GET
|/api/users/books/*book_id* |Borrow a book               |POST
|/api/auth/register        |Creates a user account      |POST
|/api/auth/login           |Logs in a user              |POST
|/api/auth/logout          |Logs out a user             |POST
|/api/auth/reset-password  |Password reset              |POST
|/api/auth/change-password  |Change password              |POST
|/api/v1/auth/authorize     |Authorize/Deauthorize a user from accessing the system(Admin Only)     |PUT
|/api/v1/auth/users         |Get a list of all the users (Admin Only)   |GET
|/api/v1/users/books/*borrow_id* |Return a Book     |PUT
|api/v1/users/books/all     |Returns all books currently loaned to all users (Admin Only)   |GET
|/api/v1/users/books    |Returns the borrowing history of a user    |GET


## Config Settings
#### Flask-Mail
- The api makes use of flask-mail to send a password reset to users
- Google SMTP services are recommended for this
- To do this, create a '.env' file in the root directory and enter the details below
```
{
    export MAIL_USERNAME='my-fake-mail@gmail.com'
    export MAIL_PASSWORD='my-fake-password'
    export MAIL_PORT=465
    export MAIL_SERVER='smtp.gmail.com'
}
```

## How to run this application

 - Clone this repository
 ```
 https://github.com/3V0L/hellobooks_api.git
 ```
 - cd into directory
 ```
 $ cd hellobooks_api
 ```
 - Install the apps dependencies by running 
 ```
 pip install -r requirements.txt
 ```
 - Open the terminal in the app's main directory
 - Run 
 ```
 python run.py
 ```

 
## How to navigate through the application endpoints
- The app makes use of JWT tokens for authentication and can take JSON requests at will.
- Postman is used to input data and get output data from the system
- PyTest is used to test the endpoints of the APIs
- First register a user with a name, email and password. After that login. Then it is possible to change password, and borrow a book under a normal user
- For the book functions you need to enter the book data in the following JSON format otherwise it will raise an error:
```
{
    "title": "War and Peace",
    "author": "Leo Tolstoy",
    "date_published": "02/12/2008",
    "genre": "fiction",
    "description": "This is a description about the book war and peace by leo tolstoy",
    "isbn": "1112223334445",
    "copies": "5"
}
```
- User data is entered in teh same format with name, password and email being used for registration
- Email and Password are used for logging
- User data is also entered in json format and should take the same format as below
```
{
    'name': 'Tapiwa',
    'email': 'john@mail.com',
    'password': 'John2018'
}
```
## Credit
*My family*

*The People at Andela*









### Made by 3V0L
