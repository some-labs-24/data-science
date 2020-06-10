import tweepy
import os

from dotenv import load_dotenv

from components.build_post_list import tweet_date_check


# TODO: If we ever get a premium API, switch num_favorites for num_replies. This is a better metric.


def calculate_engagement(twitter_handle):
    """
    Returns the number of followers, number of retweets, number of replies, and engagement ratio over the last 30 days.
    """
    load_dotenv()

    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")

    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # Get number of followers:
    num_followers = api.get_user(screen_name=twitter_handle).followers_count

    # Initialize counts:
    num_retweets = 0
    num_favorites = 0

    # Cycle through timeline and add values to count:
    timeline = api.user_timeline(screen_name=twitter_handle, count=200)
    for post in timeline:
        if tweet_date_check(post, 30):
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

    return dict(data)


if __name__ == "__main__":
    print(calculate_engagement("dutchbros"))
