import requests
import json

def get_token():
    request_url = 'https://post-route-feature.herokuapp.com/api/auth/dsteam'
    payload = {'email':'ds10@lasersharks.com', 'password':'krahs'}
    return requests.post(request_url, json=payload)