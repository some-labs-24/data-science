import requests
from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps



# Slack message from Jose Rivera:lambdapm-new:  4:14 PM
# https://social-media-strategy.herokuapp.com/ New backend end point FOR DS 
# https://social-media-strategy.herokuapp.com/api/auth/dsteam <------- TO Login in and get a TOKEN from BACKEND -- (edited) 


backend_base_url = 'social-media-strategy.herokuapp.com'
endpoint_for_for_getting_token = '/api/auth/dsteam'


# token_expected = 'access_token myToken' # Supplied by backend team
token_expected_by_backend = 'not saved in github'

def token_required(func_to_wrap):
    """Decorator used to apply 'requirement for valid token 
    to log in' to routes."""
    @wraps(func_to_wrap)
    def decorated(*args, **kwargs):
        token = request.headers['Authorization'] # Authorization is name of field holding token.
        if not token:
            return jsonify({'message' : 'Token is missing.'}), 403
        elif token != token_expected:  # TODO: replace with real validation, like against a config variable
            return jsonify({'message' : 'Token is invalid.'}), 403
        return func_to_wrap(*args, **kwargs)

    return decorated


def create_app():
    app = Flask(__name__)

    @app.route('/recommend', methods=['POST'])
    @token_required

    def recommended():
        user_input = request.get_json()
        id = user_input["id"]

        backend_url = 'https://social-media-strategy.herokuapp.com/api/posts/' + f'{id}'

        # header_data = {'Authorization' : token_expected_by_backend}
        header_data = {'Authorization' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJqZWN0Ijo2LCJlbWFpbCI6ImRzMTBAbGFzZXJzaGFya3MuY29tIiwib2t0YV91c2VyaWQiOiJEUyBoYXZlIG5vIE9rdGEiLCJpYXQiOjE1ODYzNzg0OTgsImV4cCI6MTU4ODk3MDQ5OH0.MH8RkfEYcbpzIFchet4BZZJe74MhJjIQ5ZbYhsryAbw'}

        baseline_time = {"optimal_time": "1PM"}

        r = requests.put(backend_url, headers = header_data, json=baseline_time)
        return jsonify(baseline_time)

    return app