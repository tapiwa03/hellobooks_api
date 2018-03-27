from flask import jsonify, Blueprint, request

class HelloBooks(object):


  def __init__(self):
    #creating a list containing dictionaries to act as a database
    self.users_counter = 0
    self.users_list = []

  def user_registration(self, data):
    self.users_list.append(data)
    return jsonify({'message':'Registered Successfully'})
    

