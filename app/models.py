from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class DBuser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(64), index=True, unique=True)
    campaign_id = db.Column(db.String(64), index=True, unique=True)
    consumer_key = db.Column(db.String(64), index=True, unique=True)
    consumer_key_secret = db.Column(db.String(64), index=True, unique=True)
    data_table = db.Column(db.String(64), index=True, unique=True)


class twitter_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(64), index=True, unique=True)


    def __repr__(self):
        return '<Post {}>'.format(self.body)