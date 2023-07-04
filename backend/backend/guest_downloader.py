import requests
import json
from datetime import datetime

android_api_key = ("CjulERsDeqhhjSme66ECg", "IQWdVyqFxghAtURHGeGiWAsmCAGmdW3WmbEx6Hck")
get_token_endpoint = "https://api.twitter.com/oauth2/token?grant_type=client_credentials"
activate_token_endpoint = "https://api.twitter.com/1.1/guest/activate.json"
user_to_id_endpoint = "https://api.twitter.com/graphql/oUZZZ8Oddwxs8Cd3iW3UEA/UserByScreenName?variables=%7B%22screen_name%22%3A%22{}%22%2C%22withSafetyModeUserFields%22%3Atrue%7D&features=%7B%22hidden_profile_likes_enabled%22%3Afalse%2C%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue%2C%22verified_phone_label_enabled%22%3Afalse%2C%22subscriptions_verification_info_verified_since_enabled%22%3Atrue%2C%22highlights_tweets_tab_ui_enabled%22%3Atrue%2C%22creator_subscriptions_tweet_preview_api_enabled%22%3Atrue%2C%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse%2C%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue%7D" 
timeline_endpoint = "https://api.twitter.com/graphql/pNl8WjKAvaegIoVH--FuoQ/UserTweetsAndReplies?variables=%7B%22userId%22%3A%22{}%22,%22count%22%3A40,%22includePromotedContent%22%3Atrue,%22withCommunity%22%3Atrue,%22withSuperFollowsUserFields%22%3Atrue,%22withDownvotePerspective%22%3Afalse,%22withReactionsMetadata%22%3Afalse,%22withReactionsPerspective%22%3Afalse,%22withSuperFollowsTweetFields%22%3Atrue,%22withVoice%22%3Atrue,%22withV2Timeline%22%3Atrue%7D&features=%7B%22responsive_web_twitter_blue_verified_badge_is_enabled%22%3Atrue,%22responsive_web_graphql_exclude_directive_enabled%22%3Atrue,%22verified_phone_label_enabled%22%3Afalse,%22responsive_web_graphql_timeline_navigation_enabled%22%3Atrue,%22responsive_web_graphql_skip_user_profile_image_extensions_enabled%22%3Afalse,%22tweetypie_unmention_optimization_enabled%22%3Atrue,%22vibe_api_enabled%22%3Atrue,%22responsive_web_edit_tweet_api_enabled%22%3Atrue,%22graphql_is_translatable_rweb_tweet_is_translatable_enabled%22%3Atrue,%22view_counts_everywhere_api_enabled%22%3Atrue,%22longform_notetweets_consumption_enabled%22%3Atrue,%22tweet_awards_web_tipping_enabled%22%3Afalse,%22freedom_of_speech_not_reach_fetch_enabled%22%3Afalse,%22standardized_nudges_misinfo%22%3Atrue,%22tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled%22%3Afalse,%22interactive_text_enabled%22%3Atrue,%22responsive_web_text_conversations_enabled%22%3Afalse,%22longform_notetweets_richtext_consumption_enabled%22%3Afalse,%22responsive_web_enhance_cards_enabled%22%3Afalse%7D"


def get_tweets(name: str):
    resp = requests.post(get_token_endpoint, auth=android_api_key)
    if (resp.status_code == 200):
        token = json.loads(resp.content)["access_token"]
        auth_header = {"Authorization": f"Bearer {token}"}
        activate_resp = requests.post(
                activate_token_endpoint,
                headers=auth_header
                )
        if (activate_resp.status_code != 200):
            print("failed")
            return
        guest_token = json.loads(activate_resp.content)["guest_token"]
        headers = {
                "Authorization": f"Bearer {token}",
                #"x-guest-token": "1675958319943393280",
                "x-twitter-active-user": "yes",
                "Referer": "https://twitter.com/"
                }
        user_id_response = requests.get(
                user_to_id_endpoint.format(name),
                headers=headers
                )
        if (user_id_response.status_code != 200):
            print("couldn't get user id")
            print(user_id_response.status_code)
            return
        user_id = json.loads(user_id_response.content)['data']['user']['result']['rest_id']
        timeline_response = requests.get(
                timeline_endpoint.format(user_id),
                headers=headers
                )
        if (timeline_response.status_code != 200):
            print("couldn't get content")
            print(timeline_response.status_code)
            return
        timeline = json.loads(timeline_response.content)['data']['user']['result']['timeline_v2']['timeline']['instructions']
        for instr in timeline:
            if 'entries' in instr:
                return extract_tweets(instr['entries'])
        return timeline
    else:
        print("failed")

def extract_tweets(data):
    if data:
        result = []
        for tweet in data:
            if 'content' in tweet and tweet['content']['entryType'] == 'TimelineTimelineItem' and tweet['content']['itemContent']['itemType'] == 'TimelineTweet':
                tweet_content = tweet['content']['itemContent']['tweet_results']['result']['legacy']
                user_content = tweet['content']['itemContent']['tweet_results']['result']['core']['user_results']['result']['legacy']
                retweeted = False
                tweet_text = tweet_content['full_text']
                tweet_media = []
                if 'extended_entities' in tweet_content and 'media' in tweet_content['extended_entities']:
                    for media in tweet_content['extended_entities']['media']:
                        if isinstance(media, dict) and media['type'] == 'photo':
                            tweet_media.append(media['media_url_https'])
                            tweet_text = tweet_text.replace(media['url'], '')
                link = {}
                if 'card' in tweet_content:
                    if tweet_content['card']['name'] == 'summary':
                        values = tweet_content['card']['binding_values']
                        link['url'] = tweet_content['card']['url']
                        link['domain'] = values['vanity_url']['string_value']
                        link['title'] = values['title']['string_value']
                        link['description'] = values['description']['string_value']
                        link['image'] = values['thumbnail_image']['image_value']['url']
                if 'urls' in tweet_content['entities']:
                    for url in tweet_content['entities']['urls']:
                        tweet_text = tweet_text.replace(url['url'], url['expanded_url'])
                        if 'url' in link and link['url'] == url['url']:
                            link['url'] = url['expanded_url']
                quoted_status = {}
                if 'is_quote_status' in tweet_content and tweet_content['is_quote_status']:
                    quoted = tweet['content']['itemContent']['tweet_results']['result']['quoted_status_result']['result']['legacy']
                    quoted_author = tweet['content']['itemContent']['tweet_results']['result']['quoted_status_result']['result']['core']['user_results']['result']['legacy']
                    quoted_status['id'] = quoted['id_str']
                    quoted_status['text'] = quoted['full_text']
                    quoted_status['date'] = datetime.strptime(quoted['created_at'], '%a %b %d %H:%M:%S %z %Y'),
                    quoted_status['author'] = {
                        'name': quoted_author['name'],
                        'username': quoted_author['screen_name'],
                        'avatar': quoted_author['profile_image_url_https'],
                    }
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
                        'name': user_content['name'],
                        'username': user_content['screen_name'],
                        'avatar': user_content['profile_image_url_https'],
                    },
                    'images': tweet_media if len(tweet_media) > 0 else None,
                    'link': link if 'url' in link else None,
                    'quoted': quoted_status if 'text' in quoted_status else None,
                    })
        return result
    return None
