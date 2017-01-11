import os
from flask import Flask
from flask_restful import Resource, reqparse, fields, marshal
from flask_sqlalchemy import SQLAlchemy
from app import app, api, db
from .models import User


class IndexResource(Resource):
    """
    Manage responses to the index route.
    Methods:
        GET
    """

    def get(self):
        """Return a welcome message."""
        return {'message': 'Welcome to my Bucketlist Api'}


class UserRegisterAPI(Resource):

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, required = True,
            help = 'username cannot be blank', location = 'json')
        self.reqparse.add_argument('password', required = True,
            help = 'password cannot be blank', location = 'json')
        super(UserRegisterAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        username = args['username']
        password = args['password']

        # testing if a user exists
        if User.query.filter_by(username = username).first() is not None:
            return {'message': 'invalid username or password'}
        user = User(username = username, password=password )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return {'message': '%s has been succesfully registered' % username}


class UserLoginAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('username', type = str, required = True,
            help = 'username cannot be blank', location = 'json')
        self.reqparse.add_argument('password', required = True,
            help = 'password cannot be blank', location = 'json')
        super(UserLoginAPI, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        username = args['username']
        password = args['password']
        # testing if a user details are correct
        user = User.query.filter_by(username = username).first()
        if user and user.check_password(password):
            return {'message': '%s has been succesfully logged in' % username}
        return {'message': 'invalid username or password'}



class BucketListAPI(Resource):

    def get(self, id):
        '''
        Can also get a specific bucketlist by specifying the id
        '''
        return {'message': 'None'}, 200

    def put(self, id):
        '''
        Edits the bucketlist with a specific id
        '''
        pass

    def delete(self, id):
        '''
        Deletes the bucketlist with a specific id
        '''
        pass

class BucketListRootAPI(Resource):

    def get(self):
        '''
        Gets all the bucketlists created by the user: The user have an option to specify the number of results they want to get.
        The default is set to 20 results and the maximum result is 100.
        The user can also search a bucketlist by name.
        '''
        return {'message': 'None'}, 200

    def post(self):
        '''
        Creates a new bucketlist
        '''
        pass

class BucketListItemsAPI(Resource):

    def post(self, id):
        '''
        Creates a new item in a specific bucketlist
        '''
        return {'message': 'None'}, 201

    def put(self, id, item_id):
        '''
        Edits a specific item in a bucketlist
        '''
        return {'message': 'None'}, 200

    def delete(self, id, item_id):
        '''
        Deletes a specific item in a bucketlist
        '''
        return {'message': 'None'}, 200
