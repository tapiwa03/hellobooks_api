
from flask import jsonify, Blueprint
from flask.views import MethodView
from hello_books import app
from hello_books.api.models import HelloBooks

#instantiate blueprint and assign to var books 
books = Blueprint('books', __name__)
 
@app.route('/api/v1/books', methods=['POST'])
def add_book():
    pass

@app.route('/api/v1/books/<int: id>', methods=['PUT'])
def edit_book():
    pass

@app.route('/api/v1/books/<int: id>', methods=['DELETE'])
def delete_book():
    pass

@app.route('/api/v1/books/', methods=['GET'])
def get_all_books():
    pass

@app.route('/api/v1/books/<int:id>', methods=['GET'])
def get_book_by_id():
    pass

#check if users is correct
@app.route('/api/v1/users/books/', methods=['GET'])
def borrow_book():
    pass