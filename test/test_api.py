''' Initiliaze API tests cases:
        setup the tests for the api everytime they are run'''
from flask.ext.testing import TestCase

class BucketListApiTest(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app
