'''ímport dependancies'''
import datetime
from flask import jsonify, Blueprint, request, Flask
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, get_raw_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
from hello_books import create_app
from hello_books.models.validate_model import HelloBooks
from hello_books.models.book_model import Books
from hello_books.models.user_model import User
from hello_books.models.blacklist_model import Blacklist


auth = Blueprint('auth', __name__)

@auth.route('/', methods=['Get'])
def home():
    '''Home page'''
    return jsonify({"message": "Home page"})

@auth.route('/api/v1/auth/reset-password', methods=['POST'])
def reset_password():
    '''Function to reseta user password'''
    email = request.json.get('email').strip()
    if User().reset_password(email) == True:
        return jsonify({
            'message': "Password has been changed to Pass123. Please login and change it."
        }), 201
    return jsonify({
        'message': "Email not found."
    }), 404
    

@auth.route('/api/v1/auth/register', methods=['POST'])
def register():
    '''Fuction to register a new user'''
    sent_data = request.get_json(force=True)
    if 'email' not in request.json:
        return jsonify({"message": "Please input email"})
    if 'password' not in request.json:
        return jsonify({"message": "Please input password"})
    if 'name' not in request.json:
        return jsonify({"message": "Please input name"})
    raw_data = {
        'name': sent_data['name'],
        'email': sent_data['email'],
        'password': sent_data['password']
    }
    data = {k.strip(): v.strip() for k, v in raw_data.items()}
    if User().check_email_exists(data['email']) == True:
        return jsonify({'message': 'Email Exists'})
    else:
        if HelloBooks().user_data_validation(data) == True:
            username = data['name']
            email = data['email']
            password = User().hash_password(data['password'])
            date_created = datetime.datetime.now()
            User().save(username, email, password, date_created)
            return jsonify({'message': 'Registered Successfully.'}), 201

        else:
            return jsonify(
                {'message': 'Please enter all the data in the correct format.'})



@auth.route('/api/v1/auth/login', methods=['POST'])
def login():
    '''Function for logging in'''
    sent_data = request.get_json(force=True)
    if 'email' not in request.json:
        return jsonify({"message": "Please input email"})
    if 'password' not in request.json:
        return jsonify({"message": "Please input password"})
    raw_data = {
        'email': sent_data['email'],
        'password': sent_data['password']
    }
    data = {k.strip(): v.strip() for k, v in raw_data.items()}
    return User().user_login(
        mail=data['email'],
        password=data['password']
    )



@auth.route('/api/v1/auth/change-password', methods=['PUT'])
@jwt_required
def change_password():
    '''Function for changing user password'''
    email = get_jwt_identity()
    new_password = request.json.get('new_password').strip()
    old_password = request.json.get('old_password').strip()
    return User().change_password(
        old_password=old_password,
        new_password=new_password,
        mail=email)
    
@auth.route('/api/v1/auth/authorize', methods=['PUT'])
@jwt_required
def authorize():
    '''Function for changing a user to an admin'''
    try:
        my_email = get_jwt_identity()
        email_of_user = request.json.get('email_of_user').strip()
        my_password = request.json.get('password').strip()
        return User().authorize(
            my_password=my_password,
            email_of_user=email_of_user,
            my_mail=my_email)
    except BaseException:
        return jsonify({"message": "An error occured. Please try again."})

@auth.route('/api/v1/auth/users', methods=['GET'])
@jwt_required
def get_all_users():
    '''function to get all books'''
    if 'page' in request.args:
        page = int(request.args['page'])
    else:
        page = 1
    if 'results' in request.args:
        results = int(request.args['results'])
    else:
        results = 5
    return User().get_all_users(page=page, per_page=results)
