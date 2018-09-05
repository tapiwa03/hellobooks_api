from flask import jsonify
from flask_jwt_extended import (
    create_access_token, get_jwt_identity,
    get_raw_jwt, jwt_required, get_jti
)
import datetime
from functools import wraps
from dateutil.relativedelta import relativedelta
from api import create_app, db

class Blacklist(db.Model):
    """Set token to be revoked"""

    __tablename__ = 'blacklist'
    token = db.Column(db.String(512), default=None)
    id = db.Column(db.Integer, primary_key=True)

    @staticmethod
    @jwt_required
    def logout():
        head = get_raw_jwt()['jti']
        add = Blacklist(token=head)
        db.session.add(add)
        db.session.commit()
        return jsonify({"message": "Logged out"}), 200

    @staticmethod
    def check_token(jti):
        '''Check if token has already been revoked'''
        if jti is not None:    
            if Blacklist().query.filter_by(token=jti).count() > 0:
                return False
            return True
        else:
            return False
