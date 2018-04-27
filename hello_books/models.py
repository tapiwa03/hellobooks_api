from flask import jsonify, Blueprint, request, Flask, json
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
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def save(self, data):
        db.session.add(data)
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
            user.date_modified = datetime.datetime.now()
            db.session.commit()
            return True
        except:
            return False

    def change_password(self, old_password, new_password, mail):
        user = User().query.filter_by(email=mail).first()
        if HelloBooks().password_validation({"password": new_password}) == True:
            if check_password_hash(user.password, old_password) is True:
                user.password = self.hash_password(new_password)
                user.date_modified = datetime.datetime.now()
                db.session.commit()
                return jsonify(
                    {'message': "Password has been changed"}), 201
            else:
                return jsonify({"message": "Old password does not match"}), 401
        else:
            return jsonify(
                {'message': "Password needs to be 6 characters or more"}) 

    def make_admin(self, my_password, email_of_user, my_mail):
        if self.check_email_exists(email_of_user) == True:
            normal_user = User().query.filter_by(email=email_of_user).first()
            admin_user = User().query.filter_by(email=my_mail).first()
            if check_password_hash(admin_user.password, my_password) is True:
                normal_user.is_admin = True
                normal_user.date_modified = datetime.datetime.now()
                db.session.commit()
                return jsonify(
                    {'message': "User %s is now an admin." % email_of_user}), 201
            else:
                return jsonify({"message": "Your password does not match"}), 401
        else:
            return jsonify({"message": "That email does not exist."}), 404

    def authorize(self, my_password, email_of_user, my_mail):
        if self.check_email_exists(email_of_user) == True:
            normal_user = User().query.filter_by(email=email_of_user).first()
            admin_user = User().query.filter_by(email=my_mail).first()
            if check_password_hash(admin_user.password, my_password) is True:
                if normal_user.authorized == True:
                    normal_user.authorized = False
                    normal_user.date_modified = datetime.datetime.now()
                    db.session.commit()
                    return jsonify(
                        {'message': "User %s is now Deauthorized." % email_of_user}), 201
                else: 
                    normal_user.authorized = True
                    normal_user.date_modified = datetime.datetime.now()
                    db.session.commit()
                    return jsonify(
                        {'message': "User %s is now an Authorized." % email_of_user}), 201
            else:
                return jsonify({"message": "Your password does not match"}), 401
        else:
            return jsonify({"message": "Email does not exist"}), 404

    def view_users(self):
        users = User().query.all()
        user_list = []
        for item in users:
            user = {
                "username": item.username,
                "email": item.email,
                "is_admin": item.is_admin,
                "authorized": item.authorized
            }
            user_list.append(user)
        return jsonify(userlist)


class Books(db.Model):
    '''Class containing book functions'''
    
    
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True)
    author = db.Column(db.String(60))
    date_published = db.Column(db.String(60))
    genre = db.Column(db.String(20))
    description = db.Column(db.String(200))
    copies = db.Column(db.Integer, default=1)
    isbn = db.Column(db.Integer, unique=True, index=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def save(self, data):
        '''Save/add a book'''
        db.session.add(data)
        db.session.commit()

    @staticmethod
    def delete(id):
        '''delete a book'''
        if Books().query.filter_by(id=book_id).count() == 0:
            return jsonify({"message": "Book does not exist"}), 404
        else:
            book = Books().query.filter_by(id=book_id).first()
            db.session.delete(book)
            db.session.commit()
            return jsonify({"message": "Successfully deleted."}), 200

    @staticmethod
    def get_by_id(book_id):
        '''Function for retriving a book by its Id'''
        if Books().query.filter_by(id=book_id).count() == 0:
            return False
        else:
            book = Books().query.filter_by(id=book_id).first()
            return jsonify(book), 200

    @staticmethod    
    def get_all():
        '''Function for retrieving all users'''
        books = Books().query.all()
        books_list = []
        for item in books:
            book = {
                "title": item.title,
                "author": item.author,
                "date_published": item.date_published,
                "genre": item.genre,
                "description": item.description,
                "copies": item.copies,
                "isbn": item.isbn,
            }
            books_list.append(book)
        return jsonify(books_list), 200

    def add_book(self, title, author, date_published, genre, description, isbn, copies, date_created):
        '''Function for adding a user'''
        try:
            if Books().query.filter_by(isbn=isbn).count() != 0:
                existing_book = Books().query.filter_by(isbn=isbn).first()
                existing_book.copies += 1
                db.session.commit()
                return jsonify({'message': 'Book exists, copies incremented by 1.'}),201
            else:
                new_book = Books(
                    title=title,
                    author=author,
                    date_published=date_published,
                    genre=genre,
                    description=description,
                    isbn=isbn,
                    copies=copies,
                    date_created=date_created)
                self.save(new_book)
                return jsonify(
                    {"message": "%s by %s has been added to library" % (title, author)})
        except BaseException:
           return jsonify({"message": "An error has occured."})

    def edit_book(self, title, book_id, author, date_published, genre, description, copies, isbn):
        '''Function for editing a book'''
        book = Books().query.filter_by(id=book_id).first()
        '''Check if title is entered and if it is correct'''
        try:            
            if title is not None:
                if HelloBooks().edit_book_validation({'title': title}) == True:
                    book.title = title
                else:
                    return jsonify(
                        {'message': 'Please enter a correct title above 4 characters'})
            '''check if author is entered and if it is correct'''
            if author is not None:
                if HelloBooks().edit_book_validation({'author': author}) == True:
                    book.author = author
                else:
                    return jsonify(
                        {'message': 'Please enter a correct author above 4 characters'})
            '''check if date is correctly entered'''
            if date_published is not None:
                if HelloBooks().date_validate(date_published) == True:
                    book.date_published = date_published
                else:
                    return jsonify(
                        {'message': 'Please enter a correct date format DD-MM-YYYY'})
            '''check if genre is entered correctly'''
            if genre in request.json:
                if HelloBooks().edit_book_validation({'genre': genre}) == True:
                    book.genre = genre
                else:
                    return jsonify(
                        {"message": "Please enter a genre between 4-10 characters"})
            '''check if description entered correctly'''
            if description is not None:
                if HelloBooks().edit_book_validation({'description': description}) == True:
                    book.description = description
                else:
                    return jsonify(
                        {'message': "Description should be between 4-200 characters"})
            if copies is not None:
                if HelloBooks().edit_book_validation({'copies': copies}) == True:
                    book.copies = copies
                else:
                    return jsonify(
                        {"message": "Please enter an integer for copies"})
            if isbn is not None:
                if HelloBooks().edit_book_validation({'genre': isbn}) == True:
                    book.isbn = isbn
                else:
                    return jsonify(
                        {"message": "Please enter a 13 digit ISBN."})
            book.date_modified = datetime.datetime.now()
            db.session.commit()
            return jsonify({"message": "Successfully edited %s" % book.title}), 201
        except:
            return jsonify({"message": "Error with data validation"})



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
                'maxlength': 20,
                'minlength': 4},
            'isbn': {
                'type': 'string',
                'required': True,
                'regex': '^[0-9]+$',
                'empty': False,
                'maxlength': 13,
                'minlength': 13},
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
                'maxlength': 20,
                'minlength': 4},
            'copies': {
                'type': 'string',
                'required': False,
                'regex': '^[0-9]+$',
                'empty': False,
                'maxlength': 1,
                'minlength': 3},
            'isbn': {
                'type': 'string',
                'required': False,
                'regex': '^[0-9]+$',
                'empty': False,
                'maxlength': 13,
                'minlength': 13},
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
