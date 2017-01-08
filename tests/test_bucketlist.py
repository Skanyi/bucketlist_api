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
        post_data = {'bucketlist_title': 'Hiking'}
        response = self.client.post('/bucketlists', data=post_data,
                                    headers=self.get_header())
        self.assertTrue(response.status_code == 201)
        self.assertIn(post_data['bucketlist_title'], response.get_data(as_text=True))

    def test_post_invalid_bucketlist(self):
        '''
        Ensures that a invalid POST request to /bucketlists
        will not create bucketlist but rather return a 400(Bad Request) status code.
        '''
        post_data = {}
        response = self.client.post('/bucketlists', data=post_data,
                                    headers=self.get_header())
        self.assert400(response)

    def test_put_bucketlist(self):
        '''
        Ensures that a valid PUT request to /bucketlists/<id>
        will edit and update the bucketlist in the database
        '''
        post_data = {'bucketlist_title': 'Chelsea FC'}
        response = self.client.post('/bucketlists', data=post_data,
                                    headers=self.get_header())
        put_data = {'bucketlist_title': 'Chelsea FC Players'}
        response = self.client.put('/bucketlists/1', data=put_data,
                                    headers=self.get_header())
        self.assertTrue(response.status_code == 201)
        self.assertIn(put_data['bucketlist_title'], response.get_data(as_text=True))

    def test_invalid_put_bucketlist(self):
        '''
        Ensures that a invalid PUT request to /bucketlists/<id>
        will not edit and update the bucketlist in the database but insteade return a 400: Bad Request
        '''
        post_data = {'bucketlist_title': 'Chelsea FC'}
        response = self.client.post('/bucketlists', data=post_data,
                                    headers=self.get_header())
        put_data = {}
        response = self.client.put('/bucketlists/1', data=put_data,
                                    headers=self.get_header())
        self.assert400(response)

    def test_delete_bucketlist(self):
        '''Ensures that a valid Delete request to /bucketlists/<id>
        will delete the bucket list from the database
        '''
        post_data = {'bucketlist_title': 'Chelsea FC'}
        response = self.client.post('/bucketlists', data=post_data,
                                    headers=self.get_header())
        response = self.client.delete('/bucketlists/1',
                                    headers=self.get_header())
        self.assertTrue(response.status_code == 200)
        self.assertIn('{}\n', response.get_data(as_text=True))

    def test_bucketlist_delete_not_found(self):
        '''
        Ensure that Delete request to /bucketlists/<id>
        will result in a status code of 404 when an object
        with that ID does NOT exist.
        '''
        response = self.client.delete('/bucketlists/9080000')
        self.assert404(response)

    def test_unauthorized_access(self):
        '''
        Ensures that a user cannont access other people bucketlists.
        Register a new user angie
        Create a bucket list with user steve,
        Try to access a bucketlist created by user steve using access token of angie
        '''
        # register a new test user called angie
        self.user = dict(username= 'angie', password= 'passworddd')
        response_register = self.client.post('/auth/register', data=self.user)
        response_data = json.loads(response_register.get_data(as_text=True))
        angie_token = response_data.get('Authorization')

        # create a bucketlist with user steve
        post_data = {'bucketlist_title': 'I Love Python'}
        self.client.post('/bucketlists', data=post_data,
                                    headers=self.get_header())

        # Access the bucket list with user angie
        response = self.client.get('/bucketlists/1', headers={'Authorization': angie_token})
        response = json.loads(response.get_data(as_text=True))
        self.assertEqual({'Message': 'bucketlist was not found.'}, response)
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
        response = self.client.get('/bucketlists?limit=7', headers=self.get_header())
        response = json.loads(response.get_data(as_text=True))
        self.assertLessEqual(len(response), 7)
        self.assert200(response)

        response = self.client.get('/bucketlists?limit=30', headers=self.get_header())
        response = json.loads(response.get_data(as_text=True))
        self.assertLessEqual(len(response), 30)
        self.assert200(response)

    def test_search_by_name(self):
        '''
        Ensures that a user can search a bucketlist by its name,
        Create a new bucketlist,
        Search through the bucketlists and returns bucketlist that contain the search term in their title
        '''
        post_data = {'bucketlist_title': 'Python Language'}
        response = self.client.post('/bucketlists', data=post_data,
                                    headers=self.get_header())
        # search for the bucketlist with a name
        search_response = self.client.get('/bucketlists?q=Python', headers=self.get_header())
        self.assertIn('Python', json.loads(search_response.get_data(as_text=True)))
        self.assert200(search_response)
