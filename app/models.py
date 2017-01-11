'''
Models the database classes for the api:
        user
        BucketList
        BucketListItems
'''

from app import db
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import generate_password_hash, \
     check_password_hash
import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    pw_hash = db.Column(db.String(128))
    bucket_lists = db.relationship('BucketList',
                                  backref='',
                                  passive_deletes=True)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def generate_auth_token(self, expiration = 10000):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'user_id': self.user_id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['user_id'])
        return user


    def __repr__(self):
        return '<user_id {}>'.format(self.user_id)

class BucketList(db.Model):
    __tablename__ = 'bucketlists'

    bucketlist_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id',
                                                     ondelete='CASCADE'))
    bucketlistitems = db.relationship('BucketListItems',
                                      backref='bucketlists',
                                      passive_deletes=True)


    def __init__(self, title, description, date_created, date_modified):
        self.title = title
        self.description = description
        self.date_created = date_created
        self.date_modified = date_modified
        self.created_by = created_by


    def __repr__(self):
        return '<bucketlist_id {}>'.format(self.bucketlist_id)

class BucketListItems(db.Model):
    __tablename__ = 'bucketlistsitems'

    item_id = db.Column(db.Integer, primary_key=True)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.bucketlist_id',
                                            ondelete='CASCADE'))
    title = db.Column(db.String())
    description = db.Column(db.String())
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    done = db.Column(db.Boolean, default=False)

    def __init__(self, title, description, date_created, date_modified):
        self.title = title
        self.description = description
        self.date_created = date_created
        self.date_modified = date_modified
        self.done = done


    def __repr__(self):
        return '<item_id {}>'.format(self.item_id)
