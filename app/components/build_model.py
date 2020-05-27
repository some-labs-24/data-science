from build_post_list import build_post_list

import pandas as pd

def build_model(twitter_handle, num_followers_to_scan):
    data = build_post_list(twitter_handle, num_followers_to_scan=num_followers_to_scan)

    df = pd.DataFrame.from_dict(data, orient='index')
    df = df.rename(columns={0:'tweets'})
    df['tweets'] = df['tweets'].apply(emoji_free_text)
    df['tweets'] = df['tweets'].apply(url_free_text)

    print(df.columns)


if __name__ == "__main__":
    build_model('lawrence_kimsey', 5)