from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
from tweepy.error import RateLimitError

from components.optimize_time import data_wrangling
from components.build_model import build_model
from components import db_functions
from components.calculate_engagement import calculate_engagement

import json

app = FastAPI()

# Necessary for CORS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TwitterHandleInput(BaseModel):
    """
    JSON input that takes only a twitter handle.
    """
    twitter_handle: str

    class Config:
        schema_extra = {
            "example": {
                "twitter_handle": "dutchbros",
            }
        }


class TopicModelBuildingInput(BaseModel):
    """
    JSON input for the /topic_model/schedule endpoint.
    """
    twitter_handle: str
    num_followers_to_scan: int = 500
    max_age_of_tweet: int = 7
    words_to_ignore: list = []

    class Config:
        schema_extra = {
            "example": {
                "twitter_handle": "dutchbros",
                "num_followers_to_scan": 500,
                "max_age_of_tweet": 7,
                "words_to_ignore": ["shooting", "violence"],
            }
        }


@app.get("/")
async def root():
    """
    Verifies the API is deployed, and links to the docs
    """
    return HTMLResponse("""
    <h1>SoMe Data Science API</h1>
    <p>Go to <a href="/docs">/docs</a> for documentation.</p>
    """)


@app.post('/recommend')
async def recommend(user_input: TwitterHandleInput):
    request_dict = user_input.dict()

    twitter_handle = request_dict['twitter_handle']

    dw = data_wrangling(twitter_handle, 5)
    followers_ids = dw.followers_ids()
    get_follower_data = dw.get_follower_data(followers_ids)
    optimal_time = dw.optimal_time(get_follower_data)

    baseline_time = {"optimal_time": optimal_time}

    return JSONResponse(content=baseline_time)


def background_model_building(twitter_handle, num_followers_to_scan=500, max_tweet_age=7, words_to_ignore=None):
    """
    This function is what runs in the background every time a topic modeling request is made.
    """
    if words_to_ignore is None:
        words_to_ignore = []
    db_functions.move_to_processing(twitter_handle)
    data = build_model(twitter_handle, num_followers_to_scan, max_tweet_age, words_to_ignore)
    db_functions.remove_from_processing(twitter_handle)
    db_functions.save_model_results(twitter_handle, json.dumps(data))


@app.post('/topic_model/schedule')
async def schedule(user_input: TopicModelBuildingInput, background_tasks: BackgroundTasks):
    request_dict = user_input.dict()

    twitter_handle = request_dict['twitter_handle']
    num_followers_to_scan = request_dict['num_followers_to_scan']
    max_age_of_tweet = request_dict['max_age_of_tweet']
    words_to_ignore = request_dict['words_to_ignore']

    if db_functions.is_name_in_queue(twitter_handle) or db_functions.is_name_in_processing(twitter_handle):
        data = {'success': False}
    else:
        data = {'success': True}
        db_functions.add_name_to_queue(twitter_handle)
        background_tasks.add_task(background_model_building, twitter_handle, num_followers_to_scan, max_age_of_tweet,
                                  words_to_ignore)

    return JSONResponse(content=data)


@app.post('/topic_model/status')
async def status(user_input: TwitterHandleInput):
    request_dict = user_input.dict()

    twitter_handle = request_dict['twitter_handle']

    data = {
        'success': True,
        'queued': db_functions.is_name_in_queue(twitter_handle),
        'processing': db_functions.is_name_in_processing(twitter_handle),
        'model_ready': db_functions.is_model_ready(twitter_handle)
    }

    return JSONResponse(content=data)


@app.post('/topic_model/get_topics')
async def get_topics(user_input: TwitterHandleInput):
    request_dict = user_input.dict()

    twitter_handle = request_dict['twitter_handle']

    if db_functions.is_model_ready(twitter_handle):
        data = db_functions.get_model_results(twitter_handle)
        data['success'] = True

    else:
        data = {
            'success': False,
            'topics': {
                1: [],
                2: [],
                3: [],
                4: [],
                5: []
            }
        }

    return JSONResponse(content=data)


@app.post('/engagement')
async def get_engagement(user_input: TwitterHandleInput, background_tasks: BackgroundTasks):
    request_dict = user_input.dict()

    twitter_handle = request_dict['twitter_handle']

    try:
        data = calculate_engagement(twitter_handle, wait_on_rate_limit=False)
    except RateLimitError:
        # This happens if we hit the rate limit when trying to get our user's timeline.
        # When this happens, we get the data recorded in the database. If user is not in database, return 0s.
        # Afterwards, set calculation task in background to update database when possible.
        if db_functions.is_name_in_engagement(twitter_handle):
            data = db_functions.get_engagement(twitter_handle)
        else:
            data = {'num_followers': 0, 'num_retweets': 0, 'num_favorites': 0, 'engagement_ratio': 0.0}
        background_tasks.add_task(calculate_engagement, twitter_handle, True)

    return JSONResponse(content=data)
