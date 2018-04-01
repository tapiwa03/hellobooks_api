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
        return jsonify({'message': "Book Doesnt Exist"})
    if not request.json:
        abort(400)
    if 'title' in request.json:
        book[0]['title'] = request.json['title']
    if 'author' in request.json:
        book[0]['author'] = request.json['author']
    if 'date_published' in request.json:
        book[0]['date_published'] = request.json['date_published']
    if 'genre' in request.json:
        book[0]['genre'] = request.json['genre']
    if 'description' in request.json:
        book[0]['description'] = request.json['description']

    if hello_books.add_book_validation(book[0]) == True:
        return jsonify({'book': book[0]})
    else:
        return jsonify({"message": "Please ensure correct entry of data"})



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


    

