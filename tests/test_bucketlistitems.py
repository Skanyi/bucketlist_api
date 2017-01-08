'''
Test that a user can create, edit and delete a bucketlistitem,
'''

from .test_api import BaseBucketListApiTest
from db.models import BucketList
import json

class BucketListItemsTest(BaseBucketListApiTest):

    def get_header(self):
        """
        Authenticate a user.
        Returns:
            request header with token
        """
        self.user = dict(username= 'steve', password= 'password')
        response_login = self.client.post('/auth/login', data=self.user)
        response_data = json.loads(response_login.get_data(as_text=True))
        token = response_data.get('Authorization')
        return {'Authorization': token,
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            }
