from flask import jsonify, Blueprint, request, Flask
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token
)
from cerberus import Validator
import datetime
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

app = FlaskAPI(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:test1234@localhost/testdb"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


class User(db.Model):

  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(25))
  email = db.Column(db.String(60), index=True, unique=True)
  password = db.Column(db.String(256))
  is_admin = db.Column(db.Boolean, default=False)
  authorized = db.Column(db.Boolean, default=False)


class Books(db.Model):

  __tablename__ = 'books'
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(60), unique=True)
  author = db.Column(db.String(60))
  date_published = db.Column(db.String(60))
  genre = db.Column(db.String(20), unique=True)
  description = db.Column(db.String(200))
  copies = db.Column(db.Integer)
  isbn = db.Column(db.Integer, unique=True, index=True)



class HelloBooks(object):

    def __init__(self):
        '''creating a list containing dictionaries to act as a database'''
        self.users_list = []
        self.books_list = []
        self.borrow_details = []

    """
    HELPER METHODS FOR USER VIEWS
    """

    def check_email_exists(self, search_email):
        '''check for email existence'''
        for find_email in self.users_list:
            if find_email['email'] == search_email:
                return True
        return False

    def check_email_for_login(self, search_email):
        '''this checks the list and returns the email or false'''
        for find_email in self.users_list:
            if find_email['email'] == search_email:
                return find_email
        return False

    def user_data_validation(self, dict_data):
        '''user data validation method'''
        schema = {
            'name': {
                'type': 'string',
                'required': True,
                'regex': '^[a-zA-Z0-9 ]+$',
                'empty': False,
                'maxlength': 20,
                'minlength': 4},
            'email': {
                'type': 'string',
                'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'},
            'password': {
                'type': 'string',
                'required': True,
                'maxlength': 16,
                'minlength': 6}}
        v = Validator(schema)
        v.allow_unknown = True
        return v.validate(dict_data)

    def password_validation(self, dict_data):
        '''Password validation method'''
        schema = {
            'password': {
                'type': 'string',
                'required': True,
                'maxlength': 16,
                'minlength': 6}}
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
        data['user_id'] = len(self.users_list) + 1
        data['is_admin'] = False
        data['password'] = generate_password_hash(data['password'])
        self.users_list.append(data)
        return jsonify({'message': 'Registered Successfully'})

    def user_login(self, data):
        if not self.check_email_exists(data['email']):
            return jsonify({'message': 'Email does not exist'})
        get_email_for_login = self.check_email_for_login(data['email'])
        if check_password_hash(
                get_email_for_login['password'],
                data['password']):
            access_token = create_access_token(identity=data['email'])
            return jsonify(access_token=access_token)
        else:
            return jsonify({'message': 'Wrong Credentials'})

    def view_users(self):
        return jsonify(self.users_list)
    """
    END OF AUTH CODE
    """

    """
    CODE FOR BOOKS
    """

    def add_book(self, data):
        data['book_id'] = len(self.books_list) + 1
        data['available'] = True
        self.books_list.append(data)
        return jsonify({'message': 'Book Added'})

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
        '''book data validation function'''
        schema = {
            'title': {
                'type': 'string',
                'required': True,
                'regex': '^[a-zA-Z0-9 ]+$',
                'empty': True,
                'maxlength': 25,
                'minlength': 4},
            'author': {
                'type': 'string',
                'required': True,
                'regex': '^[a-zA-Z0-9 ]+$',
                'empty': True,
                'maxlength': 25,
                'minlength': 4},
            'genre': {
                'type': 'string',
                'required': True,
                'regex': '^[a-zA-Z0-9 ]+$',
                'empty': True,
                'maxlength': 10,
                'minlength': 4},
            'description': {
                'type': 'string',
                'required': True,
                'maxlength': 200,
                'minlength': 4}}
        v = Validator(schema)
        v.allow_unknown = True
        return v.validate(dict_data)

    def edit_book_validation(self, dict_data):
        '''book data validation function using CERBERUS'''
        schema = {
            'title': {
                'type': 'string',
                'required': False,
                'empty': True,
                'regex': '^[a-zA-Z0-9 ]+$',
                'maxlength': 25,
                'minlength': 4},
            'author': {
                'type': 'string',
                'required': False,
                'regex': '^[a-zA-Z0-9 ]+$',
                'empty': True,
                'maxlength': 25,
                'minlength': 4},
            'genre': {
                'type': 'string',
                'required': False,
                'regex': '^[a-zA-Z0-9 ]+$',
                'empty': True,
                'maxlength': 10,
                'minlength': 4},
            'description': {
                'type': 'string',
                'required': False,
                'maxlength': 200,
                'minlength': 4}}
        v = Validator(schema)
        v.allow_unknown = True
        return v.validate(dict_data)

    def date_validate(self, date_text):
        try:
            datetime.datetime.strptime(date_text, '%d-%m-%Y')
            return True
        except BaseException:
            return False

    """
    END OF BOOK CODE
    """



   


if __name__ == '__main__':
    manager.run()
