import json
from .test_api import BaseBucketListApiTest

class ResourcesTest(BaseBucketListApiTest):

    def test_404(self):
        response = self.client.get('/some-wrong/url')
        self.assert404(response)

    def test_no_auth(self):
        response = self.client.get('/bucketlists')
        self.assertTrue(response.status_code == 401)
