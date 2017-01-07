import os
from flask import Flask
from flask_restful import Resource, reqparse, fields, marshal
from flask_sqlalchemy import SQLAlchemy
from app import app, api


class IndexResource(Resource):
    """
    Manage responses to the index route.
    Methods:
        GET
    """

    def get(self):
        """Return a welcome message."""
        return {'Message': 'Welcome to my api'}


class UserRegisterAPI(Resource):
    def post(self):
        return {'Message': 'None'}


class UserLoginAPI(Resource):
    def post(self):
        return {'Message': 'None'}


class BucketListAPI(Resource):

    def get(self, id=None):
        '''
        Gets all the bucketlists created: The user have an option to specify the number of results they want to get.
        The default is set to 20 results and the maximum result is 100.
        The user can also search a bucketlist by name.
        Can also get a specific bucketlist by specifying the id
        '''
        print('Awesome')
        pass

    def post(self):
        '''
        Creates a new bucketlist
        '''
        pass

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


class BucketItemsAPI(Resource):

    def post(self):
        '''
        Creates a new item in a specific bucketlist
        '''
        pass

    def put(self, id):
        '''
        Edits a specific item in a bucketlist
        '''
        pass

    def delete(self, id):
        '''
        Deletes a specific item in a bucketlist
        '''
        pass


api.add_resource(IndexResource, '/',endpoint ='index')
api.add_resource(UserRegisterAPI, '/auth/register', endpoint='register')
api.add_resource(UserLoginAPI, '/auth/login', endpoint='login')
api.add_resource(BucketListAPI, '/bucketlists', endpoint='lists')
api.add_resource(BucketListAPI, '/bucketlists/<int:id>', endpoint='list')
api.add_resource(BucketItemsAPI, '/bucketlists/<int:id>/<int:item_id>', endpoint='item')
