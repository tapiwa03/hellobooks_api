from flask import jsonify, Blueprint, request, Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
  create_access_token
  )


class HelloBooks(object):


  def __init__(self):
    #creating a list containing dictionaries to act as a database
    self.users_counter = 0
    self.users_list = []

    #list to holld all books
    self.books_list = []

  #base methods, will be used multiple times
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



    #End of base methods



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
  Code for user methods that are imported into auth_views.py
  """
  def add_book(self,data):
    self.books_list.append(data)
    return jsonify({'message' : 'Book Added'})

  def view_books(self):
    return jsonify(self.books_list)


