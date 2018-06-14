from flask import jsonify, Blueprint, request, Flask, json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, get_jwt_identity
)
import datetime
from dateutil.relativedelta import relativedelta
from hello_books import create_app, db
from hello_books.models.validate_model import HelloBooks
from hello_books.models.user_model import User


class Books(db.Model):
    '''Class containing book functions'''

    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    author = db.Column(db.String(60))
    date_published = db.Column(db.String(60))
    genre = db.Column(db.String(20))
    description = db.Column(db.String(200))
    copies = db.Column(db.Integer, default=1)
    isbn = db.Column(db.String(15), unique=True, index=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def save(self, data):
        '''Save/add a book'''
        if  User().check_user_is_admin() is False:
            return jsonify({"message": "You are not authorise to perfrom this action"}), 403
        db.session.add(data)
        db.session.commit()

    @staticmethod
    def delete(id):
        '''delete a book'''
        if  User().check_user_is_admin() is False:
            return jsonify({"message": "You are not authorise to perfrom this action"}), 403
        if Books().query.filter_by(id=id).count() == 0:
            return jsonify({"message": "Book does not exist"}), 404
        else:
            book = Books().query.filter_by(id=id).first()
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
    def get_all(page, per_page):
        '''Function for retrieving all books'''
        books = Books().query.order_by(Books.id.asc()).paginate(
            page,
            per_page,
            error_out=True)
        books_list = []
        for item in books.items:
            book = {
                "title": item.title,
                "author": item.author,
                "date_published": item.date_published,
                "genre": item.genre,
                "description": item.description,
                "copies": item.copies,
                "isbn": item.isbn
            }
            books_list.append(book)
        return jsonify(books_list), 200

    def add_book(self, title, author, date_published, genre, description, isbn, copies, date_created):
        '''Function for adding a user'''
        if  User().check_user_is_admin() is False:
            return jsonify({"message": "You are not authorise to perfrom this action"}), 403
        if Books().query.filter_by(isbn=isbn).count() != 0:
            existing_book = Books().query.filter_by(isbn=isbn).first()
            existing_book.copies += 1
            db.session.commit()
            return jsonify({'message': 'Book exists, copies incremented by 1.'}), 201
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

    @staticmethod
    def edit_book(title, book_id, author, date_published, genre, description, copies, isbn):
        '''Function for editing a book'''
        #check if user is admin
        if  User().check_user_is_admin() is False:
            return jsonify({"message": "You are not authorise to perfrom this action"}), 403
        #check if book exists
        if Books().query.filter_by(id=book_id).count() == 0:
            return jsonify({"message": 'Book not found'})
        book = Books().query.filter_by(id=book_id).first()
        '''Check if title is entered and if it is correct'''
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
                    {'message': 'Please enter a correct date format DD/MM/YYYY'})
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
