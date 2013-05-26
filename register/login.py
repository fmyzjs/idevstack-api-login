#!/usr/bin/env python
#coding=utf8

'''
Created on MAY 18, 2013

@author: zjsfmy
'''

try:
    import os
    import sys
    import urllib
    import urllib2
    import cookielib
    import base64
    import re
    import hashlib
    import json
    import rsa
    import binascii
    import time

except ImportError:
        print >> sys.stderr, """\

There was a problem importing one of the Python modules required.
The error leading to this problem was:

%s

Please install a package which provides this module, or
verify that the module is installed correctly.

It's possible that the above module doesn't match the current version of Python,
which is:

%s

""" % (sys.exc_info(), sys.version)
        sys.exit(1)


__prog__= "BISTU_API_login for python"
__site__= "http://zjsfmy.github.com"
__version__="0.1 beta"



app_key = 'yours app_key'
app_pass = 'yours app_pass'

def get_prelogin_pubkey():
    args = {
        'app_key': app_key,
        'app_pass': app_pass,
        'table': 'member',
        'action': 'getloginkey'
        }
    """
    Perform prelogin action, get prelogin status, including pubkey
    """
    prelogin_url = 'http://api.bistu.edu.cn/api/api_app.php?' + urllib.urlencode(args);
    data = urllib2.urlopen(prelogin_url).read()
    try:
        data = json.loads(data)
        pubkey = data
        return pubkey
    except:
        print 'Getting prelogin status met error!'
        return None

def login(username,passwd):
    """
    Perform login action with use name, password .
    @param username: login user name
    @param passwd: login password
    """
    #GET data 
    login_data = {
        'app_key': app_key,
        'app_pass': app_pass,
        'table': 'member',
        'action': 'login',
        'info': ''
        }
    try:
        loginkey = get_prelogin_pubkey()
    except:
        return    
    # GET data
    login_data['info'] = get_info_rsa(username, passwd, loginkey)
    login_url = 'http://api.bistu.edu.cn/api/api_app.php?' + urllib.urlencode(login_data);
    result = urllib2.urlopen(login_url)
    text = result.read()
    try:
        data = json.loads(text)
        accessToken = data['accessToken']
        user = data['username']
        idtype = data['idtype']
        return accessToken, user, idtype
    except:
        print 'Getting user info error!'
        return None


def get_info_rsa(username, passwd , loginkey):
    """
        Get rsa2 encrypted password, using RSA module from https://pypi.python.org/pypi/rsa/3.1.1, documents can be accessed at 
        http://stuvel.eu/files/python-rsa-doc/index.html
    """
    #n, n parameter of RSA public key, which is published by api.bistu.edu.cn
    #hardcoded here but you can also find it from values return from prelogin status above
    #loginKey = get_prelogin_pubkey()
    key = int(loginkey, 16)
    #e, exponent parameter of RSA public key, API uses 0x10001, which is 65537 in Decimal
    login_rsa_e = 65537
    unixtime = int(time.time())
    info = username + '|' + passwd +'|' + str(unixtime)   
    #construct API RSA Publickey using n and e above, note that n is a hex string
    key = rsa.PublicKey(key, login_rsa_e)
    #get encrypted password
    encropy_pwd = rsa.encrypt(info, key)
    #trun back encrypted password binaries to hex string
    return binascii.b2a_hex(encropy_pwd)
    