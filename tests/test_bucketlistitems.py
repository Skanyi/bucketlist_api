'''
Test that a user can create, edit and delete a bucketlistitem,
'''

from .test_api import BaseBucketListApiTest
from app.models import BucketListItems
import json

class BucketListItemsTest(BaseBucketListApiTest):

    def get_header(self):
        """
        Authenticate a user.
        Returns:
            request header with token
        """
        user = {"username": "kanyi", "password": "chelsea"}
        response_login = self.client.post('/auth/login', data=json.dumps(user))
        response_data = json.loads(response_login.get_data(as_text=True))
        token = response_data.get('Authorization')
        return {'Authorization': token,
                'Content-Type': 'application/json'
            }
    def add_bucketlist(self):
        '''
        Creates a bucketlist that will be used to test if items can be created on it
        '''
        post_data = {'title': 'Programming Language'}
        response = self.client.post('/bucketlists', data=json.dumps(post_data),
                        headers=self.get_header())
        if response.status_code == 200:
            return True
        return False

    def test_post_bucketlistitem(self):
        '''
        Ensures that a user can create a bucketlistitems in a certain bucketlist
        '''
        self.add_bucketlist()
        post_data = {'title': 'Python'}
        response = self.client.post('/bucketlists/1/items', data=json.dumps(post_data),
                                    headers=self.get_header())

        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('succesfully created', response_data['message'])

    def test_post_invalid_bucketlistitem(self):
        '''
        Ensures that a invalid POST request to /bucketlists/<id>/items
        will not create bucketlistitems but rather return a 400(Bad Request) status code.
        '''
        self.add_bucketlist()
        post_data = {'done': False}
        response = self.client.post('/bucketlists', data=json.dumps(post_data),
                                    headers=self.get_header())
        self.assert400(response)

    def test_put_bucketlistitem(self):
        '''
        Ensures that a user can edit a bucketlistitem in a certain bucketlist
        '''
        self.add_bucketlist()
        post_data = {'item': 'Python', 'done': False}
        post_response = self.client.post('/bucketlists/1/items', data=json.dumps(post_data),
                                    headers=self.get_header())
        self.assertEqual(post_response.status_code, 201)
        put_data = {'item': 'Javascript', 'done': False}
        put_response = self.client.put('/bucketlists/1/items/1', data=json.dumps(put_data),
                                        headers=self.get_header())
        self.assertEqual(put_response.status_code, 200)
        put_response_data = json.loads(put_response.get_data(as_text=True))
        self.assertIn(put_data['item'], put_response_data['message'])

    def test_invalid_put_bucketlistitem(self):
        '''
        Ensures that a invalid PUT request to /bucketlists/<bucketlist_id>/items/<item_id>
        will not edit and update the bucketlistitem in the database but insteade return a 204: No Content
        '''
        self.add_bucketlist()
        post_data = {'item': 'Chelsea FC', 'done': False}
        response = self.client.post('/bucketlists/1/items', data=json.dumps(post_data),
                                    headers=self.get_header())
        put_data = {}
        response = self.client.put('/bucketlists/1/items/1', data=json.dumps(put_data),
                                    headers=self.get_header())
        self.assertEqual(response, 204)

    def test_delete_bucketlistitems(self):
        '''
        Ensures that a user can delete a specific bucketlistitem that belong to
        a certain bucketlist
        '''
        self.add_bucketlist()
        post_data = {'item': 'Python', 'done': False}
        post_response = self.client.post('/bucketlists/1/items', data=json.dumps(post_data),
                                    headers=self.get_header())
        self.assertEqual(post_response.status_code, 201)
        delete_response = self.client.delete('/bucketlists/1/items/1',
                                                headers=self.get_header())
        self.assertTrue(delete_response.status_code == 204)
        self.assertIn('{}\n', delete_response.get_data(as_text=True))

    def test_bucketlist_delete_not_found(self):
        '''
        Ensure that Delete request to /bucketlists/<id>/items/<item_id>
        will result to a status code of 404 when an bucketlistitem
        with that ID does NOT exist.
        '''
        self.add_bucketlist()
        response = self.client.delete('/bucketlists/1/items/9080000', headers=self.get_header())
        self.assert404(response)
