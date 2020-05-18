import os
import tweepy
import sys
import datetime
import time
import json

from dotenv import load_dotenv

load_dotenv()

TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


def tweet_date_check(tweet, num_days=7):
    """
    Returns true if a tweet is newer than a certain number of days (default 7)
    """
    start_time = datetime.datetime.now() - datetime.timedelta(days=num_days)
    return ( tweet.created_at > start_time )



def build_post_list(user_screen_name, num_followers_to_scan=100):
    user_id = api.get_user(screen_name=user_screen_name).id
    followers_ids = api.followers_ids(screen_name=user_screen_name)
    followers_ids = followers_ids[0:num_followers_to_scan]

    # post_list = set()
    post_dict = dict()

    count = 0

    for follower_id in followers_ids:
        # follower_name = follower.screen_name

        try:

            # Favorites are not a good factor of engagement. Taking this part out.

            # favorites = api.favorites(user_id=follower_id)

            # for post in favorites:
            #     if post.user.id not in [user_id, follower_id]:  # We should avoid adding the app user's own posts to the list.
            #         post_list.add(post.id)

            timeline = api.user_timeline(user_id=follower_id, count=100, tweet_mode='extended')

            for post in timeline:
                if post.in_reply_to_status_id and (post.in_reply_to_user_id not in [user_id, follower_id]) and tweet_date_check(post) and post.lang == 'en':
                    replied = api.get_status(id=post.in_reply_to_status_id, tweet_mode='extended')
                    # post_list.add(post.in_reply_to_user_id)
                    post_dict[replied.id] = replied.full_text

                else:
                    try:
                       retweeted = post.retweeted_status
                       if (retweeted.user.id not in [user_id, follower_id]) and tweet_date_check(post) and post.lang == 'en':
                        #    post_list.add(retweeted.id)
                           post_dict[retweeted.id] = retweeted.full_text
                    except AttributeError:
                        pass  # This happens if a post is not a retweet. 

        except tweepy.TweepError:
            pass  # This usually happens if a user has protected tweets. No way around this, really.

        count = count + 1
        sys.stdout.write("\r" + str(count) + " out of " + str(len(followers_ids)))
        time.sleep(1)  # Makes things slow, but twitter is happier if each request is spaced out. 

    # return list(post_list)
    return post_dict



if __name__ == "__main__":
    program_start_time = time.time()
    new_list = build_post_list("elonmusk")
    # new_list = build_post_list("lawrence_kimsey")
    program_end_time = time.time()
    print("\n" + str(len(new_list)), "posts in corpus")
    print(program_end_time - program_start_time, "seconds to finish")

    # Uncomment this if you want to build a corpus for testing:

    # with open('elonmusk_followers.json', 'w') as fp:
    #     json.dump(new_list, fp)
    # fp.close()