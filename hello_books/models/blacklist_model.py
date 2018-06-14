from flask import jsonify, Blueprint, request, Flask, json
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    create_access_token, get_jwt_identity
)
import datetime
from dateutil.relativedelta import relativedelta
from hello_books import create_app, db


class Blacklist(db.Model):
    """Set token to be revoked"""

    __tablename__ = 'blacklist'
    token = db.Column(db.String(512), default=None)
    revoked = db.Column(db.Boolean, default=False)
    email = db.Column(db.String(60), unique=False, primary_key=True)

    @staticmethod
    def logout(email):
        blacklist = Blacklist().query.filter_by(email=email).first()
        blacklist.revoked = True 
        db.session.commit()
        
    @staticmethod
    def add_token(token, email):
        blacklist = Blacklist().query.filter_by(email=email).first()
        blacklist.token = token
        blacklist.revoked = False
        db.session.commit()

    @staticmethod
    def add_user(mail):
        add = Blacklist(email=mail) 
        db.session.add(add)
        db.session.commit()

    @staticmethod
    def check_token_revoked():
        email = get_jwt_identity
        blacklist = Blacklist().query.filter_by(email=email).first()
        if blacklist.revoked is True:
            return True

