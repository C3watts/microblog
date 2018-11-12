import requests

class Twitter_Authentication:
        
    oath_callback = "http%"
    oath_consumer_key = "get from configuration code"
    oath_nonce = Twitter_Authentication.construct_oath_params.nonce
    oath_signature = Twitter_Authentication.construct_oath_params.signature
    oath_signature_method = "HMAC-SHA1"
    oath_timestamp = Twitter_Authentication.construct_oath_params.timestamp
    oath_version = "1.0"
    payload = {'oauth_callback': oath_callback, "oauth_consumer_key": oath_consumer_key, "oauth_nonce": oath_nonce, "oauth_signature": oath_signature, "oauth_signature_method": oath_signature_method, "oauth_timestamp": oath_timestamp, "oauth_version": oath_version}
    url = 'HTTP/api.twitter.com/oauth/request_token'

    @classmethod 
    def construct_oath_params(cls):
        def signature()
            signature = " "
            return signature
        def nonce()
            nonce = " "
            return nonce
        def timestamp()
            timestamp = " "
            return timestamp