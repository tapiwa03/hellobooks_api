from flask import jsonify, Blueprint, request, Flask, json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token
)
import datetime
from dateutil.relativedelta import relativedelta
from hello_books import create_app, db
from hello_books.models.validate_model import HelloBooks
from hello_books.models.book_model import Books
from hello_books.models.user_model import User



class Borrow(db.Model):
    '''Class for borrowing books'''

    __tablename__ = 'borrow'
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(60))
    borrow_date = db.Column(db.String(11))
    due_date = db.Column(db.String(11))
    book_id = db.Column(db.String(20))
    date_returned = db.Column(db.String(200))

    def borrow_book(self, book_id, user_email, borrow_date, due_date, return_date):
        '''Function to borrow a book'''
        book = Books().query.filter_by(id=book_id).first()
        books_not_returned = Borrow().query.filter_by(
            user_email=user_email, date_returned=None).count()
        '''Convert dates for later comparison'''
        borrow_time = datetime.datetime.today() + relativedelta(days=40)
        due = datetime.datetime.strptime(due_date, "%d/%m/%Y")
        borrow_period = datetime.datetime.strptime(
            borrow_time.strftime("%d/%m/%Y"), "%d/%m/%Y")
        '''End of date formating'''
        if HelloBooks().date_validate(due_date) == False:
            return jsonify({"message": "Please enter a valid date"})
        if book.copies == 0:
            return jsonify(
                {"message": 'All copies of %s have been borrowed.' % book.title})
        if Books().query.filter_by(id=book_id).count() == 0:
            return jsonify({"message": 'Book not found'}), 404
        if books_not_returned > 4:
            return jsonify(
                {"message": 'you have borrowed 5 books. Please return 1 to be able to borrow another'}), 401
        if due > borrow_period:
            return jsonify(
                {"message": 'Please select a return date that is less than or equal to 40 days.'}), 401
        else:
            data = Borrow(
                user_email=user_email,
                borrow_date=borrow_date,
                due_date=due_date,
                date_returned=return_date,
                book_id=book_id
            )
            book.copies = book.copies - 1
            book.date_modified = datetime.datetime.now()
            db.session.add(data)
            db.session.commit()
            return jsonify(
                {'message': 'You have borrowed the book %s due on %s.' % (book.title, due_date)}), 201

    def return_book(self, borrow_id, user_email, return_date):
        '''function to return a book'''
        if Borrow().query.filter_by(id=borrow_id).count() == 0:
            return jsonify({"message": "There is no book borrowed under this id"}), 404
        borrow = Borrow().query.filter_by(id=borrow_id).first()
        book = Books().query.filter_by(id=borrow.book_id).first()
        if borrow.date_returned is None:
            if borrow.user_email == user_email:
                borrow.date_returned = return_date
                book.date_modified = datetime.datetime.now()
                db.session.commit()
                return jsonify({"message": "The book %s has been returned" % book.title}), 201
            return jsonify({"message": "You did not borrow this book"}), 401
        return jsonify({"message": "This book has been returned"}), 401

    def borrowing_history(self, user_email, page, per_page):
        '''Function to retrieve a users full borrowing history'''
        if Borrow().query.filter_by(user_email=user_email).count() < 1:
            return jsonify({"message": 'This user has not borrowed any books yet'}), 404
        borrow_list = []
        history = Borrow().query.filter_by(user_email=user_email).paginate(
            page,
            per_page,
            error_out=True)
        for item in history.items:
            book = Books().query.filter_by(id=item.book_id).first()
            user = User().query.filter_by(email=user_email).first()
            borrowed = {
                "borrow_id": item.id,
                "book_title": book.title,
                "isbn": book.isbn,
                "username": user.username,
                "borrow_date": item.borrow_date,
                "due_date": item.due_date,
                "date_returned": item.date_returned,
            }
            borrow_list.append(borrowed)
        return jsonify(borrow_list), 200

    def books_not_returned(self, user_email):
        '''Function to retrieve the books currently in the possession of the user'''
        if Borrow().query.filter_by(user_email=user_email).count() < 1:
            return jsonify({"message": 'This user has not borrowed any books yet'}), 404
        borrow_list = []
        history = Borrow().query.filter_by(user_email=user_email)
        for item in history:
            book = Books().query.filter_by(id=item.book_id).first()
            user = User().query.filter_by(email=user_email).first()
            borrowed = {
                "borrow_id": item.id,
                "book_title": book.title,
                "isbn": book.isbn,
                "username": user.username,
                "borrow_date": item.borrow_date,
                "due_date": item.due_date,
                "date_returned": item.date_returned,
            }
            if item.date_returned == None:
                borrow_list.append(borrowed)
        if len(borrowed) < 1:
            return jsonify({"message": "All books have been returned."}), 200
        return jsonify(borrow_list), 200
