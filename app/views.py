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
        return {'message': 'None'}


class UserRegisterAPI(Resource):
    def post(self):
        return {'message': 'None'}


class UserLoginAPI(Resource):
    def post(self):
        return {'message': 'None'}


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


api.add_resource(IndexResource, '/',endpoint ='index')
api.add_resource(UserRegisterAPI, '/auth/register', endpoint='register')
api.add_resource(UserLoginAPI, '/auth/login', endpoint='login')
api.add_resource(BucketListRootAPI, '/bucketlists', endpoint='lists')
api.add_resource(BucketListAPI, '/bucketlists/<int:id>', endpoint='list')
api.add_resource(BucketListItemsAPI, '/bucketlists/<int:id>/items', endpoint='items')
api.add_resource(BucketListItemsAPI, '/bucketlists/<int:id>/items/<int:item_id>', endpoint='item')
