from flask import Flask, request, jsonify
import requests

backend_url = 'https://post-route-feature.herokuapp.com/api/posts/:id'

def create_app():
    app = Flask(__name__)
    

    @app.route('/recommend', methods=['POST', 'GET'])
    def recommended():

        baseline_time = jsonify({
      "optimal_time": "1PM"
})
        r = requests.put(backend_url, data=baseline_time)
        return r

    return app