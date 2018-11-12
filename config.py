
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTH_TOKEN_SECRET = 'cWkZXredqhqiEkA2bUyVNxim5V7OEXTMOGOLdkLgSoJ5r'
    CONSUMER_SECRET = '2895981300-mulPderkOSJObd6p3QY9eqNFEDsagA4Hlw2aiRx'