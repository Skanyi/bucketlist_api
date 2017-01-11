'''
Test that a user can create, edit and delete a bucketlist,
Test that a user cannot access other peoples bucketlist,
Test that a user must be logged in to view their bucketlist,
Test that a user can specify the number of results returned,
Test that a user can search a bucketlist by its name
'''

from .test_api import BaseBucketListApiTest
from app.models import BucketList
import json

class BucketListTest(BaseBucketListApiTest):

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

    def test_post_bucketlist(self):
        '''
        Ensures that a valid POST request to /bucketlists
        will create a new bucketlist.
        '''
        post_data = {'title': 'Hiking'}
        response = self.client.post('/bucketlists', data=json.dumps(post_data),
                                    headers=self.get_header())
        self.assertEqual(response.status_code, 201)
        self.assertIn(post_data['title'], response.get_data(as_text=True))

    def test_post_invalid_bucketlist(self):
        '''
        Ensures that a invalid POST request to /bucketlists
        will not create bucketlist but rather return a 400(Bad Request) status code.
        '''
        post_data = {}
        response = self.client.post('/bucketlists', data=json.dumps(post_data),
                                    headers=self.get_header())
        self.assert400(response)

    def test_put_bucketlist(self):
        '''
        Ensures that a valid PUT request to /bucketlists/<id>
        will edit and update the bucketlist in the database
        '''
        post_data = {'title': 'Chelsea FC'}
        response = self.client.post('/bucketlists', data=json.dumps(post_data),
                                    headers=self.get_header())
        put_data = {'title': 'Chelsea FC Players'}
        response = self.client.put('/bucketlists/1', data=json.dumps(put_data),
                                    headers=self.get_header())
        self.assertTrue(response.status_code == 200)
        self.assertIn('was updated', response.get_data(as_text=True))

    def test_invalid_put_bucketlist(self):
        '''
        Ensures that a invalid PUT request to /bucketlists/<id>
        will not edit and update the bucketlist in the database but insteade return a 204: No Content
        '''
        post_data = {'title': 'Chelsea FC'}
        response = self.client.post('/bucketlists', data=json.dumps(post_data),
                                    headers=self.get_header())
        put_data = {}
        response = self.client.put('/bucketlists/1', data=json.dumps(put_data),
                                    headers=self.get_header())
        self.assert400(response)

    def test_delete_bucketlist(self):
        '''Ensures that a valid Delete request to /bucketlists/<id>
        will delete the bucket list from the database
        '''
        post_data = {'title': 'Chelsea FC'}
        response = self.client.post('/bucketlists', data=json.dumps(post_data),
                                    headers=self.get_header())
        response = self.client.delete('/bucketlists/1', headers=self.get_header())
        self.assertEqual(response.status_code, 204)
        self.assertIn('{}\n', response.get_data(as_text=True))

    def test_bucketlist_delete_not_found(self):
        '''
        Ensure that Delete request to /bucketlists/<id>
        will result to a status code of 404 when a bucketlist
        with that ID does NOT exist.
        '''
        response = self.client.delete('/bucketlists/9080000', headers=self.get_header())
        self.assert404(response)

    def test_unauthorized_access(self):
        '''
        Ensures that a user cannont access other people bucketlists.
        Register a new user angie
        Create a bucket list with user steve,
        Try to access a bucketlist created by user steve using access token of angie
        '''
        # register a new test user called angie
        user = {"username": "angie", "password": "chelseaddd"}
        response_register = self.client.post('/auth/register', data=json.dumps(user))
        response_data = json.loads(response_register.get_data(as_text=True))
        angie_token = response_data.get('Authorization')

        # create a bucketlist with user steve
        post_data = {'title': 'I Love Python'}
        self.client.post('/bucketlists', data=json.dumps(post_data),
                                    headers=self.get_header())

        # Access the bucket list with user angie
        response = self.client.get('/bucketlists/1', headers={'Authorization': angie_token})
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('bucketlist was not found', response_data['message'])
        self.assert404(response)

    def test_unauthenticated_access(self):
        '''
        Ensures that a user is logged in before they can access their bucketlists
        '''
        response = self.client.get('/bucketlists')
        self.assert401(response)

    def test_get_non_existing_bucketlist(self):
        response = self.client.get('/bucketlists/258642245')
        self.assert404(response)

    def test_pagination(self):
        '''
        Ensures that a user can specify the number of results they want returned
        '''
        post_data1 = {'title': 'Python Language'}
        response = self.client.post('/bucketlists', data=json.dumps(post_data1),
                                    headers=self.get_header())
        post_data2 = {'title': 'I Love Python'}
        self.client.post('/bucketlists', data=json.dumps(post_data2),
                                    headers=self.get_header())
        post_data3 = {'title': 'Chelsea FC'}
        response = self.client.post('/bucketlists', data=json.dumps(post_data3),
                                    headers=self.get_header())

        response = self.client.get('/bucketlists?limit=2', headers=self.get_header())
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 2)
        self.assert200(response)

    def test_search_by_name(self):
        '''
        Ensures that a user can search a bucketlist by its name,
        Create a new bucketlist,
        Search through the bucketlists and returns bucketlist that contain the search term in their title
        '''
        post_data = {'title': 'Python Language'}
        response = self.client.post('/bucketlists', data=json.dumps(post_data),
                                    headers=self.get_header())
        post_data3 = {'title': 'Chelsea FC'}
        response = self.client.post('/bucketlists', data=json.dumps(post_data3),
                                    headers=self.get_header())
        # search for the bucketlist with a name Python
        search_response = self.client.get('/bucketlists?q=Python', headers=self.get_header())
        search_response_data = json.loads(search_response.get_data(as_text=True))
        self.assertIn('Python', search_response_data['message'])
        self.assertNotIn('Chelsea', search_response_data['message'])
        self.assert200(search_response)
