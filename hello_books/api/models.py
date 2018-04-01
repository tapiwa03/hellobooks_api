from flask import jsonify, Blueprint, request, Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
  create_access_token
  )
from cerberus import Validator


class HelloBooks(object):


  def __init__(self):
    #creating a list containing dictionaries to act as a database
    self.users_counter = 0
    self.users_list = []

    #list to holld all books
    self.books_list = []

    #list of borrowed books
    self.borrow_details = []


  """
  HELPER METHODS FOR USER VIEWS
  """

  #check for email existence
  def check_email_exists(self, search_email):
    for find_email in self.users_list:
      if find_email['email'] == search_email:
        return True
    return False

  def check_email_for_login(self, search_email):
    #this checks the list and returns the email or false
    for find_email in self.users_list:
      if find_email['email'] == search_email:
        return find_email
    return False

  
  def user_data_validation(self, dict_data):
    schema={
        'name': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 20, 'minlength': 4},
        'email': {'type': 'string', 'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
        'password': {'type': 'string', 'required': True, 'maxlength': 16, 'minlength': 6}
    }
    v = Validator(schema)
    v.allow_unknown = True
    return v.validate(dict_data)

  def password_validation(self, dict_data):
    schema = {
        'password': {'type': 'string', 'required': True, 'maxlength': 16, 'minlength': 6}
    } 
    v = Validator(schema)
    v.allow_unknown = True
    return v.validate(dict_data)


  """
  END OF USER HELPER METHODS
  """

  """
  Code for user methods that are imported into auth_views.py
  """
  def user_registration(self, data):
    data['password'] =generate_password_hash(data['password'])
    self.users_list.append(data)
    return jsonify({'message':'Registered Successfully'})
  

  def user_login(self, data):
    if not self.check_email_exists(data['email']):
      return jsonify({'message' : 'Email does not exist'})
      
    #check if password matches
    get_email_for_login = self.check_email_for_login(data['email'])
    if check_password_hash(get_email_for_login['password'], data['password']):
      access_token = create_access_token(identity=data['email'])
      return jsonify(access_token=access_token)
    else:
      return jsonify({'message' : 'Wrong Credentials'})


  def view_users(self):
    return jsonify(self.users_list)
  """
  END OF AUTH CODE
  """


  """
  CODE FOR BOOKS
  """  

  def add_book(self,data):
    self.books_list.append(data)
    return jsonify({'message' : 'Book Added'})


  def view_books(self):
    return jsonify(self.books_list)


  def borrow_book(self, data):
    self.borrow_details.append(data)
    response = jsonify({'message': "You have borrowed this book"})
    return response

  

  """
  VALIDATION FOR BOOK DATA
  """


  def add_book_validation(self, dict_data):
    schema = {
        'title': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 25, 'minlength': 4},
        'author': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 25, 'minlength': 4},
        'genre': {'type': 'string', 'required': True, 'empty': False, 'maxlength': 10, 'minlength': 4},
        'description': {'type': 'string', 'required': False, 'maxlength': 200, 'minlength': 4},
    }
    v = Validator(schema)
    v.allow_unknown = True
    return v.validate(dict_data)

  """
  END OF BOOK CODE
  """


