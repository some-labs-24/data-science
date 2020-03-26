import requests
from flask import Flask, request, jsonify


def create_app():
    app = Flask(__name__)
    

    @app.route('/recommend', methods=['POST'])
    def recommended():
        user_input = request.get_json()
        id = user_input["id"]

        backend_url = 'https://post-route-feature.herokuapp.com/api/posts/' + f'{id}'

        baseline_time = {"optimal_time": "1PM"}

        r = requests.put(backend_url, json=baseline_time)
        return jsonify({"optimal_time": "1PM"})

    return app