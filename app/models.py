import os, random
import jwt
from datetime import datetime, date
from app import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from time import time

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    info = db.relationship('Information', backref='owner', lazy='dynamic')
    docs = db.relationship('Documents', backref='owner', lazy='dynamic')
    vid = db.relationship('VirtualID', backref='owner', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode({'reset_password': self.id, 'exp':time()+ expires_in },app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id= jwt.decode(token, app.config['SECRET_KEY'],algorithms=['HS256'])['reset_password']

        except:
            return
        return User.query.get(id)



class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(15), index=True)
    surname = db.Column(db.String(20), index=True)
    phone = db.Column(db.Integer, index=True, unique=True)
    dob = db.Column(db.DateTime, index=True)
    domicile=db.Column(db.String(25), index=True)
    tenth=db.Column(db.Integer, index=True)
    twelfth= db.Column(db.Integer, index=True)
    address = db.Column(db.String(180))
    university = db.Column(db.Integer, index=True)
    timestamp= db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Documents(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    aadhar = db.Column(db.String(100), index=True)
    tenth= db.Column(db.String(100), index=True)
    twelfth = db.Column(db.String(100), index=True)
    domicile = db.Column(db.String(100), index=True)
    birth = db.Column(db.String(100), index=True)

    def __repr__(self):
        return '<Image Path: {}>'.format(self.body)


class VirtualID(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    virtual_id=db.Column(db.Integer, index=True, unique=True)

    def __repr__(self):
        return '<VirtualID: {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

