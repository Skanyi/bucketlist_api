'''
Models the database classes for the api:
        user
        BucketList
        BucketListItems
'''

from app import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, \
     check_password_hash
import datetime

Base = declarative_base()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password_hash = db.Column(db.String(128))

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def __repr__(self):
        return '<id {}>'.format(self.id)

class BucketList(db.Model):
    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # do the relationship here that connect a user to certain bucketlist

    def __init__(self, title, description, date_created, date_modified):
        self.title = title
        self.description = description
        self.date_created = date_created
        self.date_modified = date_modified


    def __repr__(self):
        return '<id {}>'.format(self.id)

class BucketListItems(db.Model):
    __tablename__ = 'bucketlistsitems'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    date_created = db.Column(db.DateTime, server_default=db.func.now())
    date_modified = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    # do the relationship here that connect a bucketlistitem to certain bucketlist

    def __init__(self, title, description, date_created, date_modified):
        self.title = title
        self.description = description
        self.date_created = date_created
        self.date_modified = date_modified


    def __repr__(self):
        return '<id {}>'.format(self.id)
