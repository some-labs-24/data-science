import requests
import json

url = 'http://localhost:5000/recommend'
url = 'https://gt-wordcount-pro.herokuapp.com/protected'


payload = {"id" : 1}
headers = {'Authorization' : 'access_token myToken',
'content-type': 'application/json; charset=utf-8'}

r = requests.post(url, data=json.dumps(payload), headers=headers)

print(r.text)

def test():
    r = requests.post(url, data=json.dumps(payload), headers=headers)
    print(r.text)
    return r.text
