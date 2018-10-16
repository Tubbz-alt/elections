# -*- coding: utf-8 -*-

'''
Fedora elections default configuration.
'''
import os
from datetime import timedelta

# Set the time after which the session expires
PERMANENT_SESSION_LIFETIME = timedelta(hours=1)

FEDORA_ELECTIONS_ADMIN_GROUP = 'elections'

# url to the database server:
DB_URL = 'sqlite:////var/tmp/elections_dev.sqlite'


# You will want to change this for your install
SECRET_KEY = 'change me'

FAS_BASE_URL = 'https://admin.stg.fedoraproject.org/accounts/'
FAS_USERNAME = ''
FAS_PASSWORD = ''
FAS_CHECK_CERT = False


OIDC_CLIENT_SECRETS = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'client_secrets.json')
OIDC_SCOPES = ['openid', 'email', 'profile', 'fedora']
