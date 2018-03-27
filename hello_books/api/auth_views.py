
from flask import jsonify, Blueprint, request, Flask
from flask.views import MethodView
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, get_raw_jwt
)
from hello_books import app
from hello_books.api.models import HelloBooks

#set blacklist for tokens which cannot be used again
blacklist = set()
jwt = JWTManager(app)
#check if jwt token is in blacklist
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist

#instantiate blueprint and assign to var auth 
auth = Blueprint('auth', __name__)

initHelloBooks = HelloBooks()

@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    sent_data = request.get_json(force = True)
    data = {
      'user_id' : len(initHelloBooks.users_list) + 1,
      'name' : sent_data['name'],
      'email' : sent_data['email'],
      'password' : sent_data['password']
    }
    #data['user_id'] = initHelloBooks.users_counter = initHelloBooks.users_counter + 1
    return initHelloBooks.user_registration(data), 201

@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    sent_data = request.get_json(force = True)
    data = {
      'email' : sent_data['email'],
      'password' : sent_data['password']
    }
    return initHelloBooks.user_login(data),200

@app.route('/api/v1/auth/logout', methods=['POST'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({'message': 'You are now logged out'}), 200


@app.route('/api/v1/auth/reset-password', methods=['POST'])
@jwt_required
def reset_password():
    email = request.json.get('email')
    new_password = request.json.get('new_password')
    # if user email does exist
    for user in initHelloBooks.users_list:
        if email == user['email']:
            user['password'] = new_password
            return jsonify({'message': "Password has been reset"}), 201
        # if user email does not exist
    return jsonify({'message': 'Your email does not exist.'})

@app.route('/api/v1/auth/users')
@jwt_required
def view_users():
    return initHelloBooks.view_users(), 200