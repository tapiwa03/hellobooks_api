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
from . import app


'''Database setup'''
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:test1234@localhost/testdb"
SQLALCHEMY_TRACK_MODIFICATIONS = False

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
    authorized = db.Column(db.Boolean, default=True)

    def save(self, data):
        db.session.add(data)
        db.session.commit()

    def delete(self, data):
        db.session.delete(data)
        db.session.commit()

    def hash_password(self, data):
         return generate_password_hash(data)
         
    def check_email_exists(self, search_email):
        '''check for email existence'''
        if User().query.filter(User.email == search_email).count() != 0:
            return True
        return False
    
    def user_login(self, mail, password):
        '''this checks the list and returns the email or false'''
        user = User().query.filter_by(email=mail).first()
        if self.check_email_exists(mail) == False:
            return jsonify({'message': 'Email does not exist.'})
        elif self.check_email_exists(mail) == True:
            if user.authorized == True:
                if check_password_hash(user.password, password) is True:
                    access_token = create_access_token(identity=mail)
                    return jsonify(access_token=access_token), 200
                else:
                    return jsonify({'message': 'Incorrect Password.'}), 401
            else:
                return jsonify(
                    {"message": "Your account has been deactivated. Please contact a library admin."})
        else:
            return jsonify(
                {'message': 'Details match no record. Would you like to register?'})

    def reset_password(self, mail):
        try:
            user = User().query.filter_by(email=mail).first()
            user.password = User().hash_password('Pass123')
            db.session.commit()
            return True
        except:
            return False

    def change_password(self, old_password, new_password, mail):
        user = User().query.filter_by(email=mail).first()
        if HelloBooks().password_validation({"password": new_password}) == True:
            if check_password_hash(user.password, old_password) is True:
                user.password = self.hash_password(new_password)
                db.session.commit()
                return jsonify(
                    {'message': "Password has been changed"}), 201
            else:
                return jsonify({"message": "Old password does not match"}), 401
        else:
            return jsonify(
                {'message': "Password needs to be 6 characters or more"}) 


    def view_users(self):
        users = User().query.all()
        userlist = []
        for item in users:
            user = {
                "username": item.username,
                "email": item.email,
                "is_admin": item.is_admin,
                "authorized": item.authorized
            }
            userlist.append(user)
        return jsonify(userlist)


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

    def __init__(self, title, author, date_published, genre, description, copies, isbn):
        self.title = title
        self.author = author
        self.date_published = date_published
        self.genre = genre
        self.description = description
        self.copies = copies
        self.isbn = isbn

    @staticmethod
    def get_by_id(book_id):
        return Books.query.get(book_id)
    @staticmethod    
    def get_all():
        return Books.query.all()



class HelloBooks(object):

    def __init__(self):
        '''creating a list containing dictionaries to act as a database'''
        self.users_list = []
        self.books_list = []
        self.borrow_details = []

    """
    HELPER METHODS FOR USER VIEWS
    """

    

    

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
