import requests
from flask import Flask, request, jsonify

backend_url = 'https://post-route-feature.herokuapp.com/api/posts/1'

def create_app():
    app = Flask(__name__)
    

    @app.route('/recommend', methods=['POST'])
    def recommended():

        baseline_time = jsonify({"optimal_time": "1PM"})
        
        r = requests.put(backend_url, data=baseline_time)
        return "worked"

    return app