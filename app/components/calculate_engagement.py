import tweepy
import os

from dotenv import load_dotenv

from components.build_post_list import tweet_date_check
from components.db_functions import update_engagement


# TODO: If we ever get a premium API, switch num_favorites for num_replies. This is a better metric.


def calculate_engagement(twitter_handle, wait_on_rate_limit=False):
    """
    Returns the number of followers, number of retweets, number of favorites, and engagement ratio over the last 30
    days. If wait_on_rate_limit is False, will throw exception RateLimitError upon hitting rate limit.
    """
    load_dotenv()

    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")

    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=wait_on_rate_limit)

    # Get number of followers:
    num_followers = api.get_user(screen_name=twitter_handle).followers_count

    # Initialize counts:
    num_retweets = 0
    num_favorites = 0

    # Collect timeline data (might need more than one page for busy twitter accounts!)
    timeline = []
    page = 1
    keep_reading = True
    while keep_reading:
        statuses = api.user_timeline(screen_name=twitter_handle, count=200, page=page)
        if statuses:
            for status in statuses:
                if tweet_date_check(status, 30):
                    timeline.append(status)
                else:
                    # Found an old tweet, time to stop reading.
                    keep_reading = False
                    break
        else:
            # No more tweets!
            keep_reading = False
        page += 1  # next page

    print(len(timeline))

    # Cycle through timeline and add values to count:
    # timeline = api.user_timeline(screen_name=twitter_handle, count=200)
    for post in timeline:
        num_retweets += post.retweet_count
        num_favorites += post.favorite_count

    # Calculate engagement:
    try:
        engagement = round(((num_retweets + num_favorites) / num_followers) * 100, 2)
    except ZeroDivisionError:
        engagement = 0

    data = {
        "num_followers": num_followers,
        "num_retweets": num_retweets,
        "num_favorites": num_favorites,
        "engagement_ratio": engagement
    }

    update_engagement(twitter_handle, num_followers, num_retweets, num_favorites, engagement)

    return dict(data)


if __name__ == "__main__":
    print(calculate_engagement("dutchbros"))
