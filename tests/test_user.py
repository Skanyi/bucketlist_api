'''
Test that the user can register and can log in
Test that a user cannot login with bad credentials
'''
from .test_api import BaseBucketListApiTest
from db.models import User
import json

class UserTest(BaseBucketListApiTest):

    def test_user_already_exist(self):
        self.user = dict(username='steve', password='password')
        response = self.client.post('/auth/register', data=self.user)
        self.assert200(response)
        response = self.client.post('/auth/register', data=self.user)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('invalid username or password', response_data['message'])

    def test_user_can_register(self):
        self.user = dict(username='steve', password='password')
        response = self.client.post('/auth/register', data=self.user)
        self.assert200(response)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('message', response_data)
        self.assertIn('Succesfully Registered', response_data['message'])

    def test_user_can_login(self):
        self.user = dict(username='steve', password='password')
        response = self.client.post('/auth/login', data=self.user)
        self.assert200(response)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('message', response_data)
        self.assertIn('Succesfully logged in', response_data['message'])

    def test_user_cannot_login_with_wrong_username(self):
        self.user = dict(username= 'steve', password='password')
        response = self.client.post('/auth/register', data=self.user)
        self.user1 = dict(username= 'kanyi', password='password')
        response = self.client.post('/auth/login', data=self.user1)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('invalid credentials', response_data['message'])

    def test_user_cannot_login_with_wrong_password(self):
        self.user = dict(username= 'steve', password='password')
        response = self.client.post('/auth/register', data=self.user)
        self.user1 = dict(username= 'steve', password= 'pass')
        response = self.client.post('/auth/login', data=self.user1)
        response_data = json.loads(response.get_data(as_text=True))
        self.assertIn('invalid credentials', response_data['message'])
