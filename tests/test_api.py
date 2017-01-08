''' Initiliaze API tests cases:
        setup the tests for the api everytime they are run'''

from flask import Flask
from flask_testing import TestCase
from config.config import TestingConfig
from db import models
from db.models import User, BucketList
from app import db, app
import json


class BaseBucketListApiTest(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

    def setUp(self):

        db.create_all()

        # create and add a test user
        steve = User(username='steve', password='password')
        db.session.add(steve)
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):

        db.session.remove()
        db.drop_all()
