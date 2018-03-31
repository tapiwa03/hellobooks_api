
from flask import jsonify, Blueprint, request, Flask
from flask.views import MethodView
from flask_jwt_extended import (
    JWTManager, jwt_required, get_jwt_identity,
    create_access_token, get_raw_jwt
)
from werkzeug.security import generate_password_hash, check_password_hash
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


hello_books = HelloBooks()


@app.route('/api/v1/auth/reset-password', methods=['POST'])
def reset_password():
    email = request.json.get('email')
    # if user email does exist
    for user in hello_books.users_list:
        if email == user['email']:
            user['password'] = generate_password_hash("Pass123")
            return jsonify({
                'message': "Password has been changed to Pass123. Please login and change it."
                }), 201
        # if user email does not exist
    return jsonify({'message': 'Unable to reset password.'})

@app.route('/api/v1/auth/register', methods=['POST'])
def register():
    sent_data = request.get_json(force = True)
    data = {
      'user_id' : len(hello_books.users_list) + 1,
      'name' : sent_data['name'],
      'email' : sent_data['email'],
      'password' : sent_data['password']
    }
    return hello_books.user_registration(data), 201


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    sent_data = request.get_json(force = True)
    data = {
      'email' : sent_data['email'],
      'password' : sent_data['password']
    }
    return hello_books.user_login(data),200


@app.route('/api/v1/auth/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({'message': 'You are now logged out'}), 200


@app.route('/api/v1/auth/change-password', methods=['POST'])
@jwt_required
def change_password():
    email = get_jwt_identity()
    new_pword = request.json.get('new_pword')
    # if user email does exist
    for user in hello_books.users_list:
        if email == user['email']:
            user['password'] = generate_password_hash(new_pword)
            return jsonify({'message': "Password has been changed"}), 201
        # if user email does not exist
    return jsonify({'message': 'Unable to change password.'})



@app.route('/api/v1/auth/users')
@jwt_required
def view_users():
    return hello_books.view_users(), 200


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify({'hello': 'world'})
    
