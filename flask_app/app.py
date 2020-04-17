import requests
from flask import Flask, request, jsonify
import datetime
from functools import wraps

backend_base_url = 'social-media-strategy.herokuapp.com'
endpoint_for_for_getting_token = '/api/auth/dsteam'
token_expected_by_backend = 'TODO get from machine environment' 

# def token_required(func_to_wrap):
#     """Decorator used to apply 'requirement for valid token 
#     to log in' to routes."""
#     @wraps(func_to_wrap)
#     def decorated(*args, **kwargs):
#         token = request.headers['Authorization'] # Authorization is name of field holding token.
#         if not token:
#             return jsonify({'message' : 'Token is missing.'}), 403
#         elif token != token_expected:  # TODO: replace with real validation, like against a config variable
#             return jsonify({'message' : 'Token is invalid.'}), 403
#         return func_to_wrap(*args, **kwargs)

#     return decorated


def create_app():
    app = Flask(__name__)

    from .routes import recommend_time
    app.register_blueprint(recommend_time)

    return app