'''ímport dependancies'''
import datetime
from flask import jsonify, Blueprint, request, Flask
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, get_raw_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
from hello_books import app, jwt
from hello_books.models import HelloBooks,User

blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    '''check if token is blacklisted'''
    jti = decrypted_token['jti']
    return jti in blacklist

auth = Blueprint('auth', __name__)
hello_books = HelloBooks()

@app.route('/', methods=['GET'])
def home():
    '''Home page containing link to documentation'''
    return jsonify(
        {'Hello Books API': "Click here to see documentation -> https://hellobooks8.docs.apiary.io/"})


@app.route('/api/v1/auth/reset-password', methods=['POST'])
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
    

@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    '''Fuction to register a new user'''
    try:
        sent_data = request.get_json(force=True)
        raw_data = {
            'name': sent_data['name'],
            'email': sent_data['email'],
            'password': sent_data['password']
        }
        data = {k.strip(): v.strip() for k, v in raw_data.items()}
        if User().check_email_exists(data['email']) == True:
            return jsonify({'message': 'Email Exists'})
        else:
            if hello_books.user_data_validation(data) == True:
                new_user = User(
                    username = data['name'],
                    email=data['email'],
                    password=User().hash_password(data['password']),
                    date_created=datetime.datetime.now())
                User().save(new_user)
                return jsonify({'message': 'Registered Successfully.'}), 201
            else:
                return jsonify(
                    {'message': 'Please enter all the data in the correct format.'})
    except BaseException:
        return jsonify({"message": "An error occured. Please try again."}), 500


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    '''Function for logging in'''
    try:
        sent_data = request.get_json(force=True)
        raw_data = {
            'email': sent_data['email'],
            'password': sent_data['password']
        }
        data = {k.strip(): v.strip() for k, v in raw_data.items()}
        return User().user_login(
            mail=data['email'],
            password=data['password']
        )
    except BaseException:
        return jsonify(
            {'message': 'Please enter your email and password correctly'})


@app.route('/api/v1/auth/logout', methods=['GET', 'POST'])
@jwt_required
def logout():
    '''Function for logout'''
    token_identifier = get_raw_jwt()['jti']
    blacklist.add(token_identifier)
    return jsonify({'message': 'You are now logged out'}), 200


@app.route('/api/v1/auth/change-password', methods=['PUT'])
@jwt_required
def change_password():
    '''Function for changing user password'''
    try:
        email = get_jwt_identity()
        new_password = request.json.get('new_password').strip()
        old_password = request.json.get('old_password').strip()
        return User().change_password(
            old_password=old_password,
            new_password=new_password,
            mail=email)
    except BaseException:
        return jsonify({"message": "An error occured. Please try again."})


@app.route('/api/v1/auth/users', methods=['GET'])
@jwt_required
def view_users():
    '''Function for viewing all books'''
    if 'page' in request.args:
        page = int(request.args['page'])
    else:
        page = 1
    if 'results' in request.args:
        results = int(request.args['results'])
    else:
        results = 5
    return User().view_users(page=page, per_page=results), 200


@app.route('/api/v1/auth/make-admin', methods=['PUT'])
@jwt_required
def make_admin():
    '''Function for changing a user to an admin'''
    try:
        my_email = get_jwt_identity()
        email_of_user = request.json.get('email_of_user').strip()
        my_password = request.json.get('password').strip()
        return User().make_admin(
            my_password=my_password,
            email_of_user=email_of_user,
            my_mail=my_email)
    except BaseException:
        return jsonify({"message": "An error occured. Please try again."})


@app.route('/api/v1/auth/authorize', methods=['PUT'])
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
