import os
import tweepy
import sys
import datetime
import time
import json

from dotenv import load_dotenv

# TODO: Try to impliment API.statuses_lookup() function when we have 100 replies to look up. This might save some time.
# TODO: Use tweepy.Cursor to enable looking up more than 5000 followers. 

class TimelineTimer:
    """
    Timer object that is used to space out the time between api.user_timeline() requests. Default: 1.25 seconds.
    """
    def __init__(self, num_seconds_to_wait=1.25):
        self.num_seconds = num_seconds_to_wait
        self.last_request_time = datetime.datetime.now() - datetime.timedelta(seconds=self.num_seconds)

    def request_made(self):
        """
        Call after each timeline request to update the last time a timeline call was made.
        """
        self.last_request_time = datetime.datetime.now()

    def wait(self):
        """
        This will wait however many seconds (if any) needed to space out each timeline request by self.num_seconds.
        """
        time_to_wait = datetime.timedelta(seconds=self.num_seconds) - (datetime.datetime.now() - self.last_request_time)
        time_to_wait = time_to_wait.total_seconds()
        if time_to_wait > 0:
            time.sleep(time_to_wait)


def tweet_date_check(tweet, num_days=7):
    """
    Returns true if a tweet is newer than a certain number of days (default 7)
    """
    start_time = datetime.datetime.now() - datetime.timedelta(days=num_days)
    return ( tweet.created_at > start_time )



def build_post_list(user_screen_name, num_followers_to_scan=100):
    load_dotenv()

    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")

    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    user_id = api.get_user(screen_name=user_screen_name).id
    followers_ids = api.followers_ids(screen_name=user_screen_name)
    followers_ids = followers_ids[0:num_followers_to_scan]

    # post_list = set()
    post_dict = dict()

    count = 0

    timeline_timer = TimelineTimer()

    for follower_id in followers_ids:
        # follower_name = follower.screen_name

        try:
            timeline = api.user_timeline(user_id=follower_id, count=100, tweet_mode='extended')
            timeline_timer.request_made()

            for post in timeline:
                try:
                    retweeted = post.retweeted_status
                    if (retweeted.user.id not in [user_id, follower_id]) and tweet_date_check(post) and post.lang == 'en':
                           post_dict[retweeted.id] = retweeted.full_text
                except AttributeError:
                    # This happens if a tweet is not a retweet! Check if it's a comment instead.
                    if post.in_reply_to_status_id and (post.in_reply_to_user_id not in [user_id, follower_id]) and tweet_date_check(post) and post.lang == 'en':
                        replied = api.get_status(id=post.in_reply_to_status_id, tweet_mode='extended')
                        post_dict[replied.id] = replied.full_text

        except tweepy.TweepError:
            pass  # This usually happens if a user has protected tweets. No way around this, really.

        count = count + 1
        # sys.stdout.write("\r" + str(count) + " out of " + str(len(followers_ids)))
        # timeline_timer.wait()  # Makes things slow, but twitter is happier if each request is spaced out. 

    return post_dict



if __name__ == "__main__":
    program_start_time = time.time()
    new_list = build_post_list("dutchbros", 5000)
    # new_list = build_post_list("lawrence_kimsey")
    program_end_time = time.time()
    print("\n" + str(len(new_list)), "posts in corpus")
    print(program_end_time - program_start_time, "seconds to finish")

    # Uncomment this if you want to build a corpus for testing:

    # filename = "dutchbros_followers.json"

    # with open(filename, 'w') as fp:
    #     json.dump(new_list, fp)
    # fp.close()