'''
This module maps the data that will be used by the marshall when returning the
data to the user
'''

from flask_restful import fields

bucketlistitem_serializer = {
    'item_id': fields.Integer,
    'title': fields.String,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'done': fields.Boolean
}

bucketlist_serializer = {
    'bucketlist_id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'items': fields.Nested(bucketlistitem_serializer),
    'created_by': fields.Integer,
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime
}
