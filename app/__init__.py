from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS, cross_origin
import os
from config.config import configuration


app = Flask(__name__)
CORS(app)
api = Api(app, catch_all_404s=True)

app.config.from_object(configuration['default'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import models
from app.views import UserRegisterAPI, UserLoginAPI, BucketListRootAPI, BucketListAPI, BucketListItemAPI, BucketListItemsRootAPI

# api.add_resource(BucketListRootAPI, '/',endpoint ='index')
api.add_resource(UserRegisterAPI, '/auth/register', endpoint='register')
api.add_resource(UserLoginAPI, '/auth/login', endpoint='login')
api.add_resource(BucketListRootAPI, '/bucketlists', endpoint='lists')
api.add_resource(BucketListAPI, '/bucketlists/<int:bucketlist_id>', endpoint='list')
api.add_resource(BucketListItemsRootAPI, '/bucketlists/<int:bucketlist_id>/items', endpoint='items')
api.add_resource(BucketListItemAPI, '/bucketlists/<int:bucketlist_id>/items/<int:item_id>', endpoint='item')
