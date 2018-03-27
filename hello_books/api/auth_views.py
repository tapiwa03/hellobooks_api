
from flask import jsonify, Blueprint
from flask.views import MethodView
from hello_books import app
from hello_books.api.models import HelloBooks

#instantiate blueprint and assign to var auth 
auth = Blueprint('auth', __name__)
 
@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    return jsonify({'message': 'registered'})

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    return jsonify({'message': 'registered'})

@app.route('/api/v1/auth/logout')
def logout():
    return jsonify({'message': 'registered'}, methods=['POST'])

@app.route('/api/v1/auth/reset-password', methods=['POST'])
def reset_password():
    return jsonify({'message': 'registered'})