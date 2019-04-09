"""
Program: yahooQuery.py
Author: nerdyGinger (with help from Yahoo docs)
Contains the request query for the yahoo weather api
"""

import time, uuid, urllib, urllib.request, hmac, hashlib, os
from urllib.parse import quote
from base64 import b64encode
from constants import *

#import for testing
"""from dotenv import load_dotenv
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)"""


def yahooQuery(query):    
    oauth = { 'oauth_consumer_key': os.environ.get('YAHOO_CLIENT_ID'),
              'oauth_nonce': uuid.uuid4().hex,
              'oauth_signature_method': 'HMAC-SHA1',
              'oauth_timestamp': str(int(time.time())),
              'oauth_version': '1.0' }
    params = query.copy()
    params.update(oauth)
    paramsSort = [k + '=' + quote(params[k], safe='')
                  for k in sorted(params.keys())]
    
    signBaseStr = ("GET&" + BASE_URL + "&"
                  + quote("&".join(paramsSort), safe=""))
    compositeKey = (quote(os.environ.get('YAHOO_CLIENT_SECRET'), safe="") + "&")
    oauthSign = b64encode(hmac.new(bytes(compositeKey, 'utf-8'), bytes(signBaseStr, 'utf-8'),
                                   hashlib.sha1).digest())
    oauth['oauth_signature'] = oauthSign
    authHeader = "OAuth " + ", ".join(['{}="{}"'.format(k,v) for k,v in oauth.items()])
    
    url = BASE_URL + urllib.parse.urlencode(query)
    request = urllib.request.Request(url)
    request.add_header('Authorization', authHeader)
    request.add_header('X-Yahoo-App-Id', os.environ.get('YAHOO_APP_ID'))
    response = urllib.request.urlopen(request).read()
    return(response)

#test method call
#print(yahooQuery({'location': 'sioux falls', 'format': 'json'}))

                  
