from flask import jsonify, Blueprint, request, abort, make_response, session
from flask_api import FlaskAPI
from flask.views import MethodView
from hello_books import app
from hello_books.api.models import HelloBooks
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, get_raw_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
import datetime

blacklist = set()


jwt = JWTManager(app)
#check if jwt token is in blacklist


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


# instantiate blueprint and assign to var books
books = Blueprint('books', __name__)

hello_books = HelloBooks()


@app.route('/api/v1/books/<int:id>', methods=['PUT'])
def edit_book(id):
    book = [book for book in hello_books.books_list if book['book_id'] == id]
    # checking if the input is in the right format
    if len(book) == 0:
        return jsonify({'message': "Book Doesn't Exist"})
    if not request.json:
        abort(400)
    #Check if title is entered and if it is correct    
    if 'title' in request.json:
        if hello_books.add_book_validation({'title': request.json['title']}) == True:
            book[0]['title'] = request.json['title']
        else:
            return jsonify({'message': 'Please enter a correct title above 4 characters'})
    #check if author is entered and if it is correct
    if 'author' in request.json:
        if hello_books.add_book_validation({'author': request.json['author']}) == True:
            book[0]['author'] = request.json['author']
        else:
            return jsonify({'message': 'Please enter a correct author above 4 characters'})
    #check if date is correctly entered    
    if 'date_published' in request.json:
        if hello_books.date_validate(request.json['date_published']) == True:
            book[0]['date_published'] = request.json['date_published']
        else:
            return jsonify({'message': 'Please enter a correct date format DD-MM-YYYY'})
    if 'genre' in request.json:
        if hello_books.add_book_validation({'genre': request.json['genre']}) == True:
            book[0]['genre'] = request.json['genre']
        else:
            return jsonify({"message": "Please enter a genre between 4-10 characters" })
    if 'description' in request.json:
        if hello_books.add_book_validation({'description': request.json['description']}) == True:
            book[0]['description'] = request.json['description']
        else:
            return jsonify({'message' : "Description should be between 4-200 characters"})

    if hello_books.add_book_validation(book[0]) == True:
        return jsonify({'book': book[0]})
    else:
        return jsonify({"message": "Please enter book data correctly"})



@app.route('/api/v1/books', methods=['POST'])
def add_book():
    sent_data = request.get_json(force=True)
    data = {
        'book_id': len(hello_books.books_list) + 1,
        'title': sent_data.get('title'),
        'author': sent_data.get('author'),
        'date_published': sent_data.get('date_published'),
        'genre': sent_data.get('genre'),
        'description': sent_data.get('description'),
        'available': True
    }
    if HelloBooks().add_book_validation(data) == True:
        hello_books.add_book(data)
        response = jsonify({
            'book_id': data['book_id'],
            'title': data['title'],
            'author': data['author'],
            'date_published': data['date_published'],
            'genre': data['genre'],
            'description': data['description'],
            'available': True
        })
        response.status_code = 201
        return response
    else:
        return jsonify({"message": "Please enter correct book details"})


# check if users is correct
@app.route('/api/v1/users/books/<int:id>', methods=['POST', 'GET', 'PUT'])
@jwt_required
def borrow_book(id):
    #to retrieve current date
    now = datetime.datetime.now()
    email = get_jwt_identity()
    book = [book for book in hello_books.books_list if book['book_id'] == id]
    #add data to dictionary
    sent_data = request.get_json(force=True)
    data = {
        'book_id': id,
        'user_email': email,
        'borrow_date': now.strftime("%d/%m/%Y"),
        'due_date': sent_data.get('due_date'),
        'return_date': ""
    }

    if len(book) == 0:
        return jsonify({'message': "Book Doesnt Exist"})
    elif book[0]['available'] == False:
        return jsonify({'message': "The book has already been borrowed"})
    else:
        book[0]['available'] = False
        HelloBooks().borrow_book(data)
        response = jsonify({
            'book_id': data['book_id'],
            'user': data['user_email'],
            'borrow_date': data['borrow_date'],
            'due_date': data['due_date'],
            'return_date': data['return_date']
        })
        response.status_code = 201
        return response



@app.route('/api/v1/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = [book for book in hello_books.books_list if book['book_id'] == id]
    if len(book) == 0:
        return jsonify({'message': "Book Doesnt Exist"})
    hello_books.books_list.remove(book[0])
    return jsonify({'message': "Book Was Deleted"})


@app.route('/api/v1/books', methods=['GET'])
def get_all_books():
    return hello_books.view_books(), 200


@app.route('/api/v1/books/<int:id>', methods=['GET'])
def get_by_id(id):
    book = [book for book in hello_books.books_list if book['book_id'] == id]
    if len(book) == 0:
        return jsonify({'message': "Book Doesnt Exist"})
    return jsonify({'book': book[0]}), 200


    

