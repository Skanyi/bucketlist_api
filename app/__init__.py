from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
import os
from config.config import configuration

app = Flask(__name__)
api = Api(app)

app.config.from_object(configuration['default'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import models
from app.views import IndexResource, UserRegisterAPI, UserLoginAPI, BucketListRootAPI, BucketListAPI, BucketListItemsAPI

api.add_resource(IndexResource, '/',endpoint ='index')
api.add_resource(UserRegisterAPI, '/auth/register', endpoint='register')
api.add_resource(UserLoginAPI, '/auth/login', endpoint='login')
api.add_resource(BucketListRootAPI, '/bucketlists', endpoint='lists')
api.add_resource(BucketListAPI, '/bucketlists/<int:bucketlist_id>', endpoint='list')
api.add_resource(BucketListItemsAPI, '/bucketlists/<int:bucketlist_id>/items', endpoint='items')
api.add_resource(BucketListItemsAPI, '/bucketlists/<int:bucketlist_id>/items/<int:item_id>', endpoint='item')
