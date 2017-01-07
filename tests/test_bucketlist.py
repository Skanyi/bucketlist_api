'''
Test that a user can create, edit and delete a bucketlist,
Test that a user cannot access other peoples bucketlist,
Test that a user must be logged in to view their bucketlist,
Test that a user can specify the number of results returned,
Test that a user can search a bucketlist by its name
'''

from .test_api import BaseBucketListApiTest
from db.models import BucketList
import json

class UserTest(BaseBucketListApiTest):
    pass
