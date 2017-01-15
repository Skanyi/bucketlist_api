import os
from flask import Flask, g, request
from flask_restful import Resource, reqparse, marshal
from flask_sqlalchemy import SQLAlchemy
from app import app, api, db
from .models import User, BucketList, BucketListItems
from .serializers import bucketlist_serializer, bucketlistitem_serializer
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)


auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)

    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

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
            return {'message': 'user with that username already exists'}
        new_user = User(username = username, password=password)
        new_user.hash_password(password)
        db.session.add(new_user)
        db.session.commit()
        return {'message': '%s has been succesfully registered' % username}, 201


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

    @auth.login_required
    def get(self, bucketlist_id):
        '''
        Can also get a specific bucketlist by specifying the id
        '''
        user_id = g.user.user_id
        bucketlist = BucketList.query.filter_by(bucketlist_id=bucketlist_id, created_by=user_id).first()

        if bucketlist:
            return marshal(bucketlist, bucketlist_serializer)
        return {'message': 'BucketList with ID %s not found' % bucketlist_id}

    @auth.login_required
    def put(self, bucketlist_id):
        '''
        Edits the bucketlist with a specific id
        '''
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
            help = 'title cannot be blank', location = 'json')
        self.reqparse.add_argument('description', location = 'json')

        user_id = g.user.user_id
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

    @auth.login_required
    def delete(self, bucketlist_id):
        '''
        Deletes the bucketlist with a specific id
        '''
        user_id = g.user.user_id

        # testing if the bucketlist with that id exists for this user before deletion
        bucketlist = BucketList.query.filter_by(bucketlist_id = bucketlist_id, created_by=user_id).first()

        if bucketlist is None:
            return {'message': 'Bucketlist with %s id not found' % bucketlist_id}, 404

        db.session.delete(bucketlist)
        db.session.commit()
        return {'message': 'The bucketlist with ID %s was deleted' % bucketlist_id}, 204


class BucketListRootAPI(Resource):

    @auth.login_required
    def get(self):
        '''
        Gets all the bucketlists created by the user: The user have an option to specify the number of results they want to get.
        The default is set to 20 results and the maximum result is 100.
        The user can also search a bucketlist by name.
        '''
        user_id = g.user.user_id
        pagination_arguments = reqparse.RequestParser()
        pagination_arguments.add_argument('page', location="args", type=int, required=False,
                                            default=1)
        pagination_arguments.add_argument('limit', location="args", type=int, required=False,
                                      default=20)
        pagination_arguments.add_argument('q', location="args", required=False)

        args = pagination_arguments.parse_args()
        page = args['page']
        limit = args['limit']
        search_words = args['q']

        if limit >100:
            limit = 100

        if search_words:
            bucketlists_page = BucketList.query.filter(
            BucketList.created_by == user_id,
            BucketList.title.like('%' + search_words + '%')).paginate(page, limit, False)
            if bucketlists_page:
                total = bucketlists_page.pages
                has_next = bucketlists_page.has_next
                has_previous = bucketlists_page.has_prev

                if has_next:
                    next_page = str(request.url_root) + 'bucketlists?' + \
                        'q=' + str(search_words) + '&page=' + str(page + 1)
                else:
                    next_page = 'None'
                if has_previous:
                    previous_page = request.url_root + 'bucketlists?' + \
                        'q=' + str(search_words) + '&page=' + str(page - 1)
                else:
                    previous_page = 'None'
                bucketlists = bucketlists_page.items

                response = {'bucketlists': marshal(bucketlists, bucketlist_serializer),
                        'has_next': has_next,
                        'pages': total,
                        'previous_page': previous_page,
                        'next_page': next_page
                        }
                return response
            else:
                return {'message': "No bucktetlist with %s found" % search_words}

        bucketlists_page = BucketList.query.filter_by(created_by=user_id).paginate(page=page, per_page=limit, error_out=False)
        total = bucketlists_page.pages
        has_next = bucketlists_page.has_next
        has_previous = bucketlists_page.has_prev

        if has_next:
            next_page = str(request.url_root) + 'bucketlists?' + \
                'limit=' + str(limit) + '&page=' + str(page + 1)
        else:
            next_page = 'None'
        if has_previous:
            previous_page = request.url_root + 'bucketlists?' + \
                'limit=' + str(limit) + '&page=' + str(page - 1)
        else:
            previous_page = 'None'
        bucketlists = bucketlists_page.items

        response = {'bucketlists': marshal(bucketlists, bucketlist_serializer),
                'has_next': has_next,
                'pages': total,
                'previous_page': previous_page,
                'next_page': next_page
                }
        return response

    @auth.login_required
    def post(self):
        '''
        Creates a new bucketlist that belong to the user that is already logged in
        '''
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
            help = 'title cannot be blank', location = 'json')
        self.reqparse.add_argument('description', default = "",
            location = 'json')

        user_id = g.user.user_id
        args = self.reqparse.parse_args()
        title = args['title']
        description = args['description']

        # testing if the bucketlist exists for this user
        if BucketList.query.filter_by(title = title, created_by=user_id).first() is not None:
            return {'message': 'Bucketlist with that title already exists'}
        new_bucketlist = BucketList(title = title.lower(), description=description, created_by=user_id)
        db.session.add(new_bucketlist)
        db.session.commit()
        return {'message': '%s has been succesfully created' % title}, 201

class BucketListItemsRootAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
            help = 'title cannot be blank', location = 'json')
        super(BucketListItemsRootAPI, self).__init__()

    @auth.login_required
    def post(self, bucketlist_id):
        '''
        Creates a new item in a specific bucketlist, check if the bucketlist exists
        before creating a bucketlit item.
        Check if that bucketlist have another item with that name.
        '''

        user_id = g.user.user_id
        args = self.reqparse.parse_args()
        title = args['title']

        # cheking if the bucketlist with the id given exists
        if BucketList.query.filter_by(bucketlist_id=bucketlist_id, created_by=user_id).first() is None:
            return {'message': 'BucketList with ID %s not found' % bucketlist_id}

        # testing if the bucketlistitems title exists for this user
        if BucketListItems.query.filter_by(bucketlist_id=bucketlist_id, title = title).first() is not None:
            return {'message': 'Bucketlistitem name %s already exists' % title}
        new_bucketlistitem = BucketListItems(title = title, bucketlist_id=bucketlist_id)
        db.session.add(new_bucketlistitem)
        db.session.commit()
        return {'message': '%s has been succesfully created' % title}, 201


class BucketListItemAPI(Resource):

    @auth.login_required
    def put(self, bucketlist_id, item_id):
        '''
        Edits a specific item in a bucketlist:
        '''
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type = str, required = True,
            help = 'title cannot be blank', location = 'json')
        self.reqparse.add_argument('done', type = bool, location = 'json')
        user_id = g.user.user_id
        args = self.reqparse.parse_args()
        title = args['title']
        done = args['done']

        if BucketList.query.filter_by(bucketlist_id=bucketlist_id, created_by=user_id).first() is None:
            return {'message': 'BucketList with ID %s not found' % bucketlist_id}

        bucketlist_item =  BucketListItems.query.filter_by(bucketlist_id=bucketlist_id, item_id=item_id).first()

        if bucketlist_item is None:
            return {'message': 'Bucketlistitem with ID %s not found' % item_id}

        if args.title:
            bucketlist_item.title = args.title
        if args.done:
            bucketlist_item.done = args.done
        db.session.commit()
        return {'message': 'The bucketlist item with ID %s was updated' % item_id}

    @auth.login_required
    def delete(self, bucketlist_id, item_id):
        '''
        Deletes a specific item in a bucketlist
        '''
        user_id = g.user.user_id

        # check that the bucketlist item is found on that bucketlist before deleting
        if BucketList.query.filter_by(bucketlist_id=bucketlist_id, created_by=user_id).first() is None:
            return {'message': 'BucketList with ID %s not found' % bucketlist_id}

        bucketlist_item = BucketListItems.query.filter_by(bucketlist_id=bucketlist_id, item_id=item_id).first()
        if bucketlist_item is None:
            return {'message': 'Bucketlistitem with ID %s not found' % item_id}, 404
        db.session.delete(bucketlist_item)
        db.session.commit()
        return {'message': 'The bucketlist item with ID %s was deleted' % item_id}, 204
