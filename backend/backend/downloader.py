import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

headers = {
    "Host": "syndication.twitter.com",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-GB,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "TE": "trailers"
}


def get_tweets(name: str):
    url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{name}"
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find("script", {"id": "__NEXT_DATA__"})
    return extract_tweets(data)


def get_tweets_and_replies(name: str):
    url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{name}?showReplies=true"
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find("script", {"id": "__NEXT_DATA__"})
    return extract_tweets(data)


def extract_tweets(data):
    if data:
        jsondata = json.loads(data.text)
        timeline = jsondata['props']['pageProps']['timeline']['entries']
        result = []
        for tweet in timeline:
            if tweet['type'] == 'tweet':
                tweet_content = tweet['content']['tweet']
                retweeted = False
                if 'retweeted_status' in tweet_content:
                    retweeted = True
                    tweet_content = tweet_content['retweeted_status']
                tweet_media = []
                if 'extended_entities' in tweet_content and 'media' in tweet_content['extended_entities']:
                    for media in tweet_content['extended_entities']['media']:
                        if isinstance(media, dict) and media['type'] == 'photo':
                            tweet_media.append(media['media_url_https'])
                tweet_text = tweet_content['full_text'];
                if 'urls' in tweet_content['entities']:
                    for url in tweet_content['entities']['urls']:
                        tweet_text = tweet_text.replace(url['url'], url['expanded_url'])
                result.append({
                    'id': tweet_content['id_str'],
                    'text': tweet_text,
                    'favs': tweet_content['favorite_count'],
                    'quotes': tweet_content['quote_count'],
                    'replies': tweet_content['reply_count'],
                    'retweets': tweet_content['retweet_count'],
                    'date':  datetime.strptime(tweet_content['created_at'], '%a %b %d %H:%M:%S %z %Y'),
                    'retweeted': retweeted,
                    'author': {
                        'name': tweet_content['user']['name'],
                        'username': tweet_content['user']['screen_name'],
                        'avatar': tweet_content['user']['profile_image_url_https'],
                    },
                    'images': tweet_media if len(tweet_media) > 0 else None
                    })
        return result
    return None
