from flask import Blueprint, request, jsonify
from .optimize_time import data_wrangling   # Look into relative imports

import requests 
import os
from dotenv import load_dotenv

load_dotenv()
BACKEND_AUTHORIZATION = os.getenv("BACKEND_AUTHORIZATION")

recommend_time = Blueprint('recommend_time', __name__)

@recommend_time.route('/recommend', methods=['POST'])
def recommendation():
    user_input = request.get_json()
    _id = user_input['id']
    twitter_handle = user_input['screenname']

    backend_url = 'https://api.so-me.net/api/posts/' + str(_id)
    header_data = {'Authorization' : BACKEND_AUTHORIZATION}

    dw = data_wrangling(twitter_handle, 5)
    followers_ids = dw.followers_ids()
    get_follower_data = dw.get_follower_data(followers_ids)
    optimal_time = dw.optimal_time(get_follower_data)

    baseline_time = {"optimal_time": optimal_time}

    r = requests.put(backend_url, headers = header_data, json=baseline_time)
    
    return jsonify(baseline_time)