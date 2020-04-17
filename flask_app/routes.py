from flask import Blueprint, request, jsonify
from .optimize_time import data_wrangling   # Look into relative imports

import datetime
import logging
import requests 

recommend_time = Blueprint('recommend_time', __name__)

@recommend_time.route('/recommend', methods=['POST'])
def recommendation():
    user_input = request.get_json()
    _id = user_input['id']
    twitter_handle = user_input['screen_name']

    backend_url = 'https://social-media-strategy.herokuapp.com/api/posts/' + str(_id)
    header_data = {'Authorization' : 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWJqZWN0Ijo2LCJlbWFpbCI6ImRzMTBAbGFzZXJzaGFya3MuY29tIiwib2t0YV91c2VyaWQiOiJEUyBoYXZlIG5vIE9rdGEiLCJpYXQiOjE1ODYzNzg0OTgsImV4cCI6MTU4ODk3MDQ5OH0.MH8RkfEYcbpzIFchet4BZZJe74MhJjIQ5ZbYhsryAbw'}

    dw = data_wrangling(twitter_handle, 5)
    fi = dw.followers_ids()
    get_follower_data = dw.get_follower_data(fi)
    optimal_time = dw.optimal_time(get_follower_data)

    baseline_time = {"optimal_time": optimal_time}

    r = requests.put(backend_url, headers = header_data, json=baseline_time)
    
    return jsonify(baseline_time)