https://travis-ci.org/3V0L/bootcamp-c2.svg?branch=ch-create-folder-structure-156303944

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

## How to run this application

 - Clone this repository
 - Set up a virtual environment
 - Install the apps dependencies by running `pip install -r requirements.txt`
 - Open the terminal in the app's main directory
 - Run `python run.py`

 
## How to run this application
-The app makes use of JWT tokens for authentication and can take JSON requests at will.
-Postman is used to input data and get output data from the system
-PyTest is usd to test the endpoints of the APIs


## Made by 3V0L