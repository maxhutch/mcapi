import requests
import getpass
import os
import json


class NoAPIKey(Exception):
    pass

params = {'apikey': ''}
baseurl = os.getenv('MCURL', 'https://materialscommons.org/api/v2')


class MCObject(object):
    """
    Attributes
    ----------
      id: str
        ID of the object
        
      name: str      
        Name of the object
      
      description: str
        Description of the object
      
      ctime: int
        Creation time of the object
        
      mtime: int
        Last modification time
        
    """
    def __init__(self):
        self.id
        self.name
        self.description
        self.ctime
        self.mtime
    

def init():
    global params
    user = getpass.getuser()
    mcapi_key_path = os.path.join(os.path.expanduser('~' + user), '.mcapikey')
    if not os.path.exists(mcapi_key_path):
        raise NoAPIKey()
    with open(mcapi_key_path, 'r') as fd:
        userapikey = fd.read()
        params['apikey'] = userapikey.strip()


def get(restpath):
    r = requests.get(make_url(restpath), params=params, verify=False)
    if r.status_code == requests.codes.ok:
        return r.json()
    r.raise_for_status()


def post(restpath, data):
    r = requests.post(make_url(restpath), params=params, verify=False, json=data)
    if r.status_code == requests.codes.ok:
        return r.json()
    r.raise_for_status()


def make_url(restpath):
    p = baseurl + '/' + restpath
    return p