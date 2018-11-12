
import requests
import random
import time
import hmac
from hashlib import sha1
import urllib
import string
import urlparse
import sqlalchemy
from models import DBuser, Post, User
from app import db
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

class Twitter:
    oauth_token = '2361748680-5Wvq0LUFVxAt9yMuVShzjEqebGKvJAaPhTrr6g9'
    oauth_token_secret = 'LgRlsrhhq7aesfLw8CKzGxxhTUZmfpBh8kONTkTbAeYLH'
    CONSUMER_SECRET = "8HvLiocLdCxcjY3ejBRZKnO4mwI8AuX25lZAFE0jJjRZfFOqsJ"

    @classmethod
    def get_params(cls, additional_params = {}):
        oauth_consumer_key = "8qxF6aWZGyxv9MBTkJZmgFTp4"
        oauth_nonce = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(32))
        oauth_signature = ''
        oauth_signature_method = "HMAC-SHA1"
        oauth_timestamp = int(time.time())
        oauth_version = "1.0"
        
        CONSUMER_SECRET = "3HssekN9DoKpDWeHGWO50PkBfrliI7yJhYt7eKnpuyW4ZOvWnb"
        if(additional_params != {}):
            additional_params.update({"oauth_consumer_key": str(oauth_consumer_key),
            "oauth_nonce": str(oauth_nonce),
            "oauth_signature_method": str(oauth_signature_method),
            "oauth_token": str(Twitter.oauth_token),
            "oauth_timestamp": str(oauth_timestamp),
            "oauth_version": str(oauth_version)
            })
            return additional_params

        return {
            "oauth_consumer_key": str(oauth_consumer_key),
            "oauth_nonce": str(oauth_nonce),
            "oauth_signature_method": str(oauth_signature_method),
            "oauth_token": str(Twitter.oauth_token),
            "oauth_timestamp": str(oauth_timestamp),
            "oauth_version": str(oauth_version)
        }

    @classmethod
    def construct_signature(cls, url, http_method, params_list, params_dict, oauth_token_secret = ""):
        print "signature param list:"
        print params_list
        signing_key = urllib.quote(Twitter.CONSUMER_SECRET, safe = '') + "&" 
        if(oauth_token_secret!= ""):
            signing_key = signing_key + urllib.quote(oauth_token_secret, safe = '')
        for key in sorted(params_dict.keys()):
            params_dict[key] =  urllib.quote(params_dict[key], safe='')
        print "signature param dict:"
        print params_dict
        print "signing_key:"
        print signing_key
        parameter_string = ""
        for key in params_list:
            parameter_string = parameter_string + key
            parameter_string = parameter_string + "=" + str(params_dict.get(key)) + "&"
        parameter_string = parameter_string[:-1]
        signature_base_string = http_method + "&" + urllib.quote(url, safe='') + "&" + urllib.quote(parameter_string, safe = '')
        print "signature_base_string:\n" + signature_base_string
        oauth_signature = hmac.new(signing_key, signature_base_string, sha1).digest().encode("base64").rstrip('\n')
        return oauth_signature

    @classmethod
    def construct_payload(cls, url, params_dict, getpost):
        payload =  Twitter.get_params()
        original_payload_keys = payload.keys()
        payload.update(params_dict)
        payload_list = sorted(payload.keys())
        oauth_signature = Twitter.construct_signature(url, getpost, list(payload_list), dict(payload), Twitter.oauth_token_secret)
        payload.update({"oauth_signature":str(oauth_signature)})
        original_payload_keys.append("oauth_signature")
        payload_list = sorted(original_payload_keys)
        return payload_list, payload


    @classmethod
    def send_request(cls, url, payload_list, payload, params_dict= {}, http_method='GET'):
        DST = "OAuth "
        for key in payload_list:
            DST = DST + urllib.quote(key, safe='') + "= \"" + urllib.quote(str(payload.get(key)), safe='') + "\", "
        print("DST:\n" + DST)
        if (params_dict == {}):
            r = requests.request(http_method, url, headers={'Authorization': DST})
        else:
            print params_dict
            r = requests.request(http_method, url, headers={'Authorization': DST}, params = params_dict)
        return(r)

    @classmethod
    def get_request_token(cls):
        url = 'https://api.twitter.com/oauth/request_token'
        payload = Twitter.get_params({"oauth_callback":"https://www.app.factivate.com/auth/twitter/callback"})
        payload.pop("oauth_token")
        payload_list = sorted(payload.keys())
        oauth_signature = Twitter.construct_signature(url, "GET", payload_list, payload)
        payload_list.append("oauth_signature")
        payload.update({"oauth_signature":oauth_signature})
        payload["oauth_callback"]="https://www.app.factivate.com/auth/twitter/callback"
        r = Twitter.send_request(url, payload_list, payload, {})
        print (r.text)
        r_dict = dict(urlparse.parse_qsl(r.text))
        oauth_token = r_dict.get("oauth_token")
        oauth_token_secret = r_dict.get("oauth_token_secret")
        return(oauth_token, oauth_token_secret)

    @classmethod
    def get_access_token(cls, oauth_verifier):
        url = 'https://api.twitter.com/oauth/access_token'
        payload =  Twitter.create_params(url)
        payload_list = sorted(payload.keys())
        oauth_signature = Twitter.construct_signature(url, "POST", payload_list, payload)
        payload.update({"oauth_signature":oauth_signature})
        payload_list.append("oauth_signature")
        params={'oauth_verifier': oauth_verifier}
        r = Twitter.send_request(url, payload_list, payload, params)
        print r.text
        r_dict = dict(urlparse.parse_qsl(r.text))
        access_token = r_dict.get("oauth_token")
        access_token_secret = r_dict.get("oauth_token_secret")
        user_id = r_dict.get("user_id")
        screen_name = r_dict.get("screen_name")
        return(access_token, access_token_secret, user_id, screen_name)

    @classmethod
    def create_sandbox_account(cls):
        url = 'https://ads-api-sandbox.twitter.com/4/accounts/'
        r = Twitter.put_together_request({}, "GET", url)
        r_dict = dict(urlparse.parse_qsl(r.text))
        return(r)

    @classmethod
    def get_sandbox_account(cls):
        url = 'https://ads-api-sandbox.twitter.com/4/accounts/gq1iff'
        r = Twitter.put_together_request({}, "GET", url)
        return(r)


    @classmethod
    def create_funding_instrument(cls):
        url = 'https://ads-api-sandbox.twitter.com/4/accounts/gq1ib4/funding_instruments' #gq1i6e
        params_dict = {
            'currency': "USD",
            'start_time':urllib.quote("2017-05-19T07:00:00Z", safe=''),
             'type': "CREDIT_CARD"
             }
        r = Twitter.put_together_request(params_dict, "POST", url)

        r_dict = dict(urlparse.parse_qsl(r.text))
        return() 


    @classmethod
    def check_funding_instrument(cls):
        url = 'https://ads-api-sandbox.twitter.com/4/accounts/gq1iff/funding_instruments' #gq1i6e
        r = Twitter.put_together_request({}, "GET", url)
        return()

    @classmethod
    def add_account_feature(cls):
        url = 'https://ads-api-sandbox.twitter.com/4/accounts/gq1ib4/features' #gq1i6e
        params_dict = {'feature_keys': "AGE_TARGETING"}
        r = Twitter.put_together_request(params_dict, "POST", url)
        return(r) 
            
    @classmethod
    def create_campaign(cls, campaign_name, start_time):
        url = 'https://ads-api-sandbox.twitter.com/4/accounts/gq1iff/campaigns' #gq1i6e
        params_dict = {
            'funding_instrument_id': "hya5e",
            "name": campaign_name,
            "start_time": start_time
            }
        r = Twitter.put_together_request(params_dict, "POST", url)
        r_dict = dict(urlparse.parse_qsl(r.text))
        return(r) 

    @classmethod
    def get_campaigns(cls):
        url = 'https://ads-api-sandbox.twitter.com/4/accounts/gq1iff/campaigns' #gq1i6e
        r = put_together_request({}, "GET", url)
        r_dict = dict(urlparse.parse_qsl(r.text))
        return(r) 



    @classmethod
    def put_together_request(cls, params_dict, getpost, url):   
        payload_list, payload = Twitter.construct_payload(url, params_dict, getpost)
        r = Twitter.send_request(url, payload_list, payload, params_dict, getpost)
        return r

    @classmethod    
    def get_campaign_data(cls, campaign_id, start_time, end_time, metric_groups):
        url = 'https://ads-api-sandbox.twitter.com/4/stats/accounts/gq1iff/'
        params_dict = {
            'end_time': end_time,
            "entity": "CAMPAIGN",
            "entity_ids": campaign_id,
            "granularity":  "HOUR", 
            "metric_groups":metric_groups,
            "placement":"ALL_ON_TWITTER",
            "start_time":start_time,
        }
        r = Twitter.put_together_request(params_dict,"GET", url)
        #r_dict = dict(urlparse.parse_qsl(r.text))
        return(r)
    
    @classmethod
    def get_from_account(cls, data):
        r = Twitter.get_campaign_data()
        print "data: " + r.json()['data'][data] + "\n"
        return()

    @classmethod
    def get_from_campaign(cls, campaign_id, data, metric_groups):
        start_time = "2018-09-08T21:00:00Z"
        end_time = "2018-09-10T21:00:00Z"
        r = Twitter.get_sandbox_account(campaign_id, start_time, end_time, metric_groups)
        print "data: " + r.json()['data'][data] + "\n"
        return(r.json()['data'][data])

    @classmethod
    def put_data_into_db(cls, name, metric_group, dict_keys, values_dict):
        engine = create_engine('sqlite:///app.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        metadata = MetaData()
        Base = declarative_base(engine)
        Base.metadata.create_all(engine)
        table_list = [name, metadata]
        for i in range (0,len(dict_keys)):
            table_list.append(Column(dict_keys[i], Integer))
        table_tuple = tuple(table_list)       
        user = Table(*table_tuple)
        user.create(engine)
        stmt = metadata.tables[name].insert().values(values_dict)
        connection = engine.connect()
        result = connection.execute(stmt)
        return result


    @classmethod
    def get_user_from_db(cls, user_id):
        #currently works with 'gq1iff'
        engine = create_engine('sqlite:///app.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        connection = engine.connect()
        u = session.query(DBuser).filter_by(account_id=user_id).first()
        print (u.id, u.account_id, u.campaign_id)
        #eventually will add u.consumer_key and u.consumer_key_secret
        return u.account_id, u.campaign_id

    @classmethod
    def get_data_from_user(cls, account_id, campaign_id, metric_group, name):
        #account_id, campaign_id = Twitter.get_user_from_db(user_id)
        #campaign_id = 'i6qx'
        start_time = "2018-09-08T21:00:00Z"
        end_time = "2018-09-10T21:00:00Z"
        data = Twitter.get_campaign_data(campaign_id, start_time, end_time, metric_group)
        print (data.json()['data'])
        dict_keys = data.json()['data'][0]['id_data'][0]['metrics'].keys()
        values_dict = data.json()['data'][0]['id_data'][0]['metrics']
        result = Twitter.put_data_into_db(name, 'ENGAGEMENT', dict_keys, values_dict)
        #display_table
        Twitter.attach_table_to_user(account_id, name)
        return values_dict

    @classmethod
    def attach_table_to_user(cls, account_id1, table_name):
        engine = create_engine('sqlite:///app.db')
        Session = sessionmaker(bind=engine)
        session = Session()
        connection = engine.connect()
        u = session.query(DBuser).filter_by(account_id=account_id1).first()
        #if(u.data_table):
            #old_table = session.query.filter_by(id=u.data_table).first()
            #print(old_table)
            #return old_table
        u.data_table = table_name
        print u.data_table
        session.query
        return

