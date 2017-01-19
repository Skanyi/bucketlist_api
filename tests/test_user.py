'''
Test that the user can register and can log in
Test that a user cannot login with bad credentials
'''
from .test_api import BaseBucketListApiTest
from app.models import User
import json

class UserTest(BaseBucketListApiTest):

    def test_user_already_exist(self):
        user = {"username": "kanyi", "password": "chelsea"}
        response = self.client.post('/auth/register', data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response = self.client.post('/auth/register', data=json.dumps(user), content_type='application/json')
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('user with that username already exists', response_data['message'])

    def test_register(self):
        user = {"username": "Kanyi", "password": "chelsea"}
        response = self.client.post('/auth/register', data=json.dumps(user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('message', response_data)
        self.assertIn('succesfully registered', response_data['message'])

    def test_login(self):
        user = {"username": "steve", "password": "password"}
        response = self.client.post('/auth/login', data=json.dumps(user), content_type='application/json')
        self.assert200(response)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('Authorization', response_data)

    def test_invalid_username(self):
        user1 = {"username": "kanyi", "password": "password"}
        response = self.client.post('/auth/login', data=json.dumps(user1), content_type='application/json')
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('invalid username or password', response_data['message'])

    def test_invalid_password(self):
        user1 = {"username": "steve", "password": "passwo"}
        response = self.client.post('/auth/login', data=json.dumps(user1), content_type='application/json')
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('invalid username or password', response_data['message'])
