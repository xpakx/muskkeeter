import requests
import json
from datetime import datetime

headers = {
    "Host": "cdn.syndication.twimg.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
    "Accept": "*/*",
    "Accept-Language": "en-GB,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Origin": "https://platform.twitter.com",
    "Connection": "keep-alive",
    "Referer": "https://cdn.syndication.twimg.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors"
}


def get_tweet(id: str):
    url = f"https://cdn.syndication.twimg.com/tweet-result?id={id}&lang=en"
    data = requests.get(url, headers=headers).content
    if data:
        tweet = json.loads(data)
        tweet_media = []
        return {
            'id': tweet['id_str'],
            'text': tweet['text'],
            'favs': tweet['favorite_count'],
            'quotes': 0,
            'replies': tweet['conversation_count'],
            'retweets': 0,
            'date':  tweet['created_at'],
            'retweeted': False,
            'author': {
                'name': tweet['user']['name'],
                'username': tweet['user']['screen_name'],
                'avatar': tweet['user']['profile_image_url_https'],
            },
            'images': tweet_media if len(tweet_media) > 0 else None
        }
    return None
