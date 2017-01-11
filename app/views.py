import os
from flask import Flask
from flask_restful import Resource, reqparse, fields, marshal
from flask_sqlalchemy import SQLAlchemy
from app import app, api, db
from .models import User, BucketList
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


auth = HTTPBasicAuth()

current_user = {
    'user_id': 4
}

@auth.verify_password
def verify_auth_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None # valid token, but expired
    except BadSignature:
        return None # invalid token
    user_id = data['id']
    current_user['user_id'] = user_id
    return user_id


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
        new_user = User(username = username, password=password )
        new_user.hash_password(password)
        db.session.add(new_user)
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
        if user and user.verify_password(password):
            token = user.generate_auth_token()
            return {'Authorization': token.decode('ascii')}
        return {'message': 'invalid username or password'}


class BucketListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
            help = 'title cannot be blank', location = 'json')
        self.reqparse.add_argument('description', location = 'json')
        super(BucketListAPI, self).__init__()

    def get(self, bucketlist_id):
        '''
        Can also get a specific bucketlist by specifying the id
        '''
        return {'message': 'None'}, 200

    #@auth.login_required
    def put(self, bucketlist_id):
        '''
        Edits the bucketlist with a specific id
        '''
        user_id = current_user['user_id']
        args = self.reqparse.parse_args()
        new_title = args['title']
        new_description = args['description']

        # testing if the bucketlist with that id exists for this user
        bucketlist = BucketList.query.filter_by(bucketlist_id = bucketlist_id, created_by=user_id).first()

        if bucketlist is None:
            return {'message': 'Bucketlist with %s id not found' % bucketlist_id}

        if args.title:
            bucketlist.title = args.title
        if args.description:
            bucketlist.description = args.description
        db.session.commit()
        return {'message': 'The bucketlist with ID %s was updated' % bucketlist_id}

    #@auth.login_required
    def delete(self, bucketlist_id):
        '''
        Deletes the bucketlist with a specific id
        '''
        user_id = current_user['user_id']
        args = self.reqparse.parse_args()

        # testing if the bucketlist with that id exists for this user before deletion
        bucketlist = BucketList.query.filter_by(bucketlist_id = bucketlist_id, created_by=user_id).first()

        if bucketlist is None:
            return {'message': 'Bucketlist with %s id not found' % bucketlist_id}

        db.session.delete(bucketlist)
        db.session.commit()
        return {'message': 'The bucketlist with ID %s was deleted' % bucketlist_id}


class BucketListRootAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
            help = 'title cannot be blank', location = 'json')
        self.reqparse.add_argument('description', default = "",
            location = 'json')
        super(BucketListRootAPI, self).__init__()

    def get(self):
        '''
        Gets all the bucketlists created by the user: The user have an option to specify the number of results they want to get.
        The default is set to 20 results and the maximum result is 100.
        The user can also search a bucketlist by name.
        '''
        return {'message': 'None'}, 200

    #@auth.login_required
    def post(self):
        '''
        Creates a new bucketlist that belong to the user that is already logged in
        '''
        user_id = current_user['user_id']
        args = self.reqparse.parse_args()
        title = args['title']
        description = args['description']

        # testing if the bucketlist exists for this user
        if BucketList.query.filter_by(title = title, created_by=user_id).first() is not None:
            return {'message': 'Bucketlist with that title already exists'}
        new_bucketlist = BucketList(title = title, description=description, created_by=current_user['user_id'])
        db.session.add(new_bucketlist)
        db.session.commit()
        return {'message': '%s has been succesfully created' % title}

class BucketListItemsAPI(Resource):

    def post(self, bucketlist_id):
        '''
        Creates a new item in a specific bucketlist
        '''
        return {'message': 'None'}, 201

    def put(self, bucketlist_id, item_id):
        '''
        Edits a specific item in a bucketlist
        '''
        return {'message': 'None'}, 200

    def delete(self, bucketlist_id, item_id):
        '''
        Deletes a specific item in a bucketlist
        '''
        return {'message': 'None'}, 200
