''' Initiliaze API tests cases:
    setup the tests for the api everytime they are run
'''

from flask_testing import TestCase
from config.config import configuration
from app.models import User
from app import db, app

class BaseBucketListApiTest(TestCase):

    def create_app(self, app=app):
        app.config.from_object(configuration['testing'])
        return app

    def setUp(self):
        self.client = self.create_app().test_client()
        db.create_all()

        # create and add a test user
        steve = User(username='steve', password='password')
        db.session.add(steve)
        db.session.commit()

    def tearDown(self):
        db.drop_all()
