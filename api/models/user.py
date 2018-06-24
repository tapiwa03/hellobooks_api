'''Import dependancies'''
import re
import datetime
from flask import jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, get_jwt_identity,
    get_jti, get_raw_jwt, JWTManager, jwt_required,
)
from flask_mail import Message
from api import db, flask_mail
from api.models.validate import HelloBooks
from api.models.blacklist import Blacklist


class User(db.Model):
    '''Class for user functions'''

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25))
    email = db.Column(db.String(60), index=True, unique=True)
    password = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    authorized = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def save(self, username, email, password, date_created):
        '''Insert data into users table'''
        if User().query.filter_by(email=email).count() > 0:
            return jsonify({'message': 'Email Exists'})
        if "@yandex" not in email:
            user = User(
                username=username,
                email=email,
                password=password,
                date_created=date_created,
                is_admin=False)
            db.session.add(user)
            db.session.commit()
        else:
            admin = User(
                username=username,
                email=email,
                password=password,
                date_created=date_created,
                is_admin=True)
            db.session.add(admin)
            db.session.commit()

    @jwt_required
    def check_token(self):
        '''Check if token is valid'''
        jti = get_raw_jwt()['jti']
        if Blacklist().check_token(jti) is False:
            return abort(401, 'You are not logged in.')

    def hash_password(self, data):
        '''Generate a password hash'''
        return generate_password_hash(data)

    @staticmethod
    def check_email_exists(search_email):
        '''check for email existence'''
        if User().query.filter_by(email=search_email).count() == 0:
            return abort(404, 'Email does not exist')

    @staticmethod
    def check_user_is_admin():
        '''Check if user is admin'''
        mail = get_jwt_identity()
        user = User().query.filter_by(email=mail).first()
        if user.is_admin is False:
            return abort(403, 'User is not an administrator')

    def user_login(self, mail, password):
        '''this checks the list and returns the email or false'''
        user = User().query.filter_by(email=mail).first()
        self.check_email_exists(mail)
        if user.authorized is True:
            if check_password_hash(user.password, password) is True:
                access_token = create_access_token(identity=mail)
                return jsonify(access_token=access_token), 200
            else:
                return jsonify({'message': 'Incorrect Password.'}), 401
        else:
            return jsonify(
                {"message": "Your account has been deactivated. Please contact a library admin."}), 403

    def reset_password(self, mail, new_password):
        '''Reset user password'''
        user = User().query.filter_by(email=mail).first()
        user.password = User().hash_password(new_password)
        user.date_modified = datetime.datetime.now()
        db.session.commit()
        msg = Message('Password Reset', sender='do-not-reply@gmail.com', recipients = [mail])
        msg.body = "Hello %s,\nYour password has been reset to:\n%s." %(user.username, new_password)
        flask_mail.send(msg)
        return jsonify({"message": "New password sent to %s" % user.username}), 200

    def change_password(self, old_password, new_password, mail):
        '''Change user password'''
        self.check_token()
        user = User().query.filter_by(email=mail).first()
        if HelloBooks().password_validation({"password": new_password}) is True:
            if check_password_hash(user.password, old_password) is True:
                user.password = self.hash_password(new_password)
                user.date_modified = datetime.datetime.now()
                db.session.commit()
                return jsonify(
                    {'message': "Password has been changed"}), 201
            else:
                return jsonify({"message": "Old password does not match"}), 401
        else:
            return jsonify(
                {'message': "Password needs to be 6 characters or more"})

    def authorize(self, my_password, email_of_user, my_mail):
        '''Authorize a user'''
        self.check_token()
        self.check_user_is_admin()
        self.check_email_exists(email_of_user)
        normal_user = User().query.filter_by(email=email_of_user).first()
        admin_user = User().query.filter_by(email=my_mail).first()
        if check_password_hash(admin_user.password, my_password) is True:
            if normal_user.authorized is True:
                normal_user.authorized = False
                normal_user.date_modified = datetime.datetime.now()
                db.session.commit()
                return jsonify(
                    {'message': "User %s is now Deauthorized." % email_of_user}), 201
            else:
                normal_user.authorized = True
                normal_user.date_modified = datetime.datetime.now()
                db.session.commit()
                return jsonify(
                    {'message': "User %s is now an Authorized." % email_of_user}), 201
        else:
            return jsonify({"message": "Your password does not match"}), 401

    def get_all_users(self, page, per_page):
        '''Function for retrieving all books'''
        self.check_token()
        self.check_user_is_admin()
        users = User().query.order_by(User.id.asc()).paginate(
            page,
            per_page,
            error_out=True)
        user_list = []
        for item in users.items:
            book = {
                "id": item.id,
                "username": item.username,
                "email": item.email,
                "admin": item.is_admin,
                "date_created": item.date_created
            }
            user_list.append(book)
        return jsonify(user_list), 200