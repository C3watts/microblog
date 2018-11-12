import unittest
from app import app
from app.twitter import Twitter
import requests

class TwitterTestCase(unittest.TestCase):

    def test_get_request_token(self):
        token, secret = Twitter.get_request_token()
        self.assertTrue(len(token)>3 and len(secret)>3)

    def test_put_together_requests(self):
        url = 'https://ads-api-sandbox.twitter.com/4/accounts/'
        params_dict = {}
        r = Twitter.put_together_request(params_dict, "GET", url)
        self.assertTrue(r.status_code == 200)

    def test_put_together_requests2(self):
        print "\n"
        url = 'https://ads-api-sandbox.twitter.com/4/accounts/gq1ib4/features'
        params_dict = {'feature_keys': "AGE_TARGETING", "start_time": "2018-09-08T21:00:00Z"}
        r = Twitter.put_together_request(params_dict, "POST", url)
        self.assertTrue(r.status_code == 200)

    
        


if __name__ == '__main__':
    unittest.main()