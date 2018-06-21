from flask import jsonify, request, Flask, json, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, get_jwt_identity,
    get_jti, get_raw_jwt, JWTManager, jwt_required,
)
import datetime
from dateutil.relativedelta import relativedelta
from api import create_app, db, flask_mail
from api.models.validate import HelloBooks
from api.models.blacklist import Blacklist
from flask_mail import Message

class User(db.Model):

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25))
    email = db.Column(db.String(60), index=True, unique=True)
    password = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean, default=False)
    authorized = db.Column(db.Boolean, default=True)
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)

    def save(self,username, email, password, date_created):
        if "@yandex.com" in email:
            admin = User(
                    username = username,
                    email=email,
                    password=password,
                    date_created=date_created,
                    is_admin=True)
            db.session.add(admin)
            db.session.commit()
        else:
            user = User(
                username = username,
                email=email,
                password=password,
                date_created=date_created,
                is_admin=True)
            db.session.add(user)
            db.session.commit()
        
    @jwt_required
    def check_token(self):
        '''Check if token is valid'''
        jti = get_raw_jwt()['jti']
        if Blacklist().check_token(jti) == False:
                return False

    def hash_password(self, data):
        '''Generate a password hash'''
        return generate_password_hash(data)

    def check_email_exists(self, search_email):
        '''check for email existence'''
        if User().query.filter(User.email == search_email).count() != 0:
            return True
        return False

    @staticmethod
    def check_user_is_admin():
        '''Check if user is admin'''
        mail = get_jwt_identity()
        user = User().query.filter_by(email=mail).first()
        if user.is_admin == False:
            return False

    def user_login(self, mail, password):
        '''this checks the list and returns the email or false'''
        user = User().query.filter_by(email=mail).first()
        if self.check_email_exists(mail) == False:
            return jsonify({'message': 'Email does not exist.'}), 404
        elif self.check_email_exists(mail) == True:
            if user.authorized == True:
                if check_password_hash(user.password, password) is True:
                    access_token = create_access_token(identity=mail)
                    return jsonify(access_token=access_token), 200
                else:
                    return jsonify({'message': 'Incorrect Password.'}), 401
            else:
                return jsonify(
                    {"message": "Your account has been deactivated. Please contact a library admin."}),403
        else:
            return jsonify(
                {'message': 'Details match no record. Would you like to register?'})

    def reset_password(self, mail, new_password):
        '''Reset user password'''
        user = User().query.filter_by(email=mail).first()
        user.password = User().hash_password(new_password)
        user.date_modified = datetime.datetime.now()
        db.session.commit()
        msg = Message('Password Reset', sender = 'do-not-reply@gmail.com', recipients = [mail])
        msg.body = "Hello %s,\nYour password has been reset to:\n %s." %(user.username, new_password)
        flask_mail.send(msg)
        return jsonify({"message": "New password sent to %s" % user.username}), 200

    def change_password(self, old_password, new_password, mail):
        '''Change user password'''
        if self.check_token() == False:
            return jsonify({"message":"You are not logged in."}), 403
        user = User().query.filter_by(email=mail).first()
        if HelloBooks().password_validation({"password": new_password}) == True:
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
        if self.check_token() is False:
            return jsonify({"message":"You are not logged in."}), 403
        if self.check_user_is_admin() is False:
            return jsonify({"message": "You are not authorise to perfrom this action"}), 403
        if self.check_email_exists(email_of_user) is True:
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
        else:
            return jsonify({"message": "Email does not exist"}), 404


    def get_all_users(self, page, per_page):
        '''Function for retrieving all books'''
        if self.check_token() is False:
            return jsonify({"message":"You are not logged in."}), 403
        if self.check_user_is_admin() is False:
            return jsonify({"message": "You are not authorise to perfrom this action"}), 403
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