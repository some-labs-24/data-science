import requests
from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps

# token_expected = 'access_token myToken' # Supplied by backend team
token_expected_by_backend = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJqZWN0IjoyOSwiZW1haWwiOiJkczEwQGxhc2Vyc2hhcmtzLmNvbSIsIm9rdGFfdXNlcmlkIjoiRFMgaGF2ZSBubyBPa3RhIiwiaWF0IjoxNTg1Njk5MTU3LCJleHAiOjE1ODgyOTExNTd9.V7lAN61UrWZRDwJg-V9Xuy8G9Bw4EVyHkYVW1xGfLPA' # Supplied by backend team


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

        backend_url = 'https://post-route-feature.herokuapp.com/api/posts/' + f'{id}'

        header_data = {'Authorization' : token_expected_by_backend}
        header_data = {'Authorization' : '123'}

        baseline_time = {"optimal_time": "1PM"}

        r = requests.put(backend_url, headers = header_data, json=baseline_time)
        return jsonify(baseline_time)

    return app