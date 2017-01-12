'''
Models the database classes for the api:
        user
        BucketList
        BucketListItems
'''

from app import db, app
from sqlalchemy.dialects.postgresql import JSON
from passlib.apps import custom_app_context as pwd_context
import datetime
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer)

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
        self.hash_password(password)

    def hash_password(self, password):
        self.pw_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.pw_hash)

    def generate_auth_token(self, expiration = 10000):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'user_id': self.user_id })


    def __repr__(self):
        return '<user_id {}>'.format(self.user_id)

class BucketList(db.Model):
    __tablename__ = 'bucketlists'

    bucketlist_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    created_by = db.Column(db.Integer, db.ForeignKey('users.user_id',
                                                     ondelete='CASCADE'))
    items = db.relationship('BucketListItems',
                                      backref='bucketlists',
                                      passive_deletes=True)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())


    def __init__(self, title, description, created_by):
        self.title = title
        self.description = description
        self.created_by = created_by


    def __repr__(self):
        return '<bucketlist_id {}>'.format(self.bucketlist_id)

class BucketListItems(db.Model):
    __tablename__ = 'bucketlistsitems'

    item_id = db.Column(db.Integer, primary_key=True)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.bucketlist_id',
                                            ondelete='CASCADE'))
    title = db.Column(db.String())
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    done = db.Column(db.Boolean, default=False)

    def __init__(self, bucketlist_id, title, done=False):
        self.bucketlist_id = bucketlist_id
        self.title = title
        self.done = done



    def __repr__(self):
        return '<item_id {}>'.format(self.item_id)
