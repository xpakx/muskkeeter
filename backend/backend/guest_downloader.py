import requests
import json
from datetime import datetime

android_api_key = ("CjulERsDeqhhjSme66ECg", "IQWdVyqFxghAtURHGeGiWAsmCAGmdW3WmbEx6Hck")
get_token_endpoint = "https://api.twitter.com/oauth2/token?grant_type=client_credentials"
activate_token_endpoint = "https://api.twitter.com/1.1/guest/activate.json"
user_to_id_endpoint = "https://api.twitter.com/graphql/oUZZZ8Oddwxs8Cd3iW3UEA/UserByScreenName"
timeline_replies_endpoint = "https://api.twitter.com/graphql/pNl8WjKAvaegIoVH--FuoQ/UserTweetsAndReplies"
timeline_endpoint = "https://api.twitter.com/graphql/rIIwMe1ObkGh_ByBtTCtRQ/UserTweets" 


def get_user_to_id_params(name: str):
    return {
            "variables": json.dumps({
                "screen_name": name,
                "withSafetyModeUserFields": True
                }),

            "features": json.dumps({
                "hidden_profile_likes_enabled": False,
                "responsive_web_graphql_exclude_directive_enabled":  True,
                "verified_phone_label_enabled": False,
                "subscriptions_verification_info_verified_since_enabled": True,
                "highlights_tweets_tab_ui_enabled": True,
                "creator_subscriptions_tweet_preview_api_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True
                })
            }


def get_timeline_replies_endpoint_params(id: int):
    return {
            "variables": json.dumps({
                "userId": id,
                "count": 40,
                "includePromotedContent": True,
                "withCommunity": True,
                "withSuperFollowsUserFields": True,
                "withDownvotePerspective": False,
                "withReactionsMetadata": False,
                "withReactionsPerspective": False,
                "withSuperFollowsTweetFields": True,
                "withVoice": True,
                "withV2Timeline": False
                }),
            "features": json.dumps({
                "responsive_web_twitter_blue_verified_badge_is_enabled": True,
                "responsive_web_graphql_exclude_directive_enabled": True,
                "verified_phone_label_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "tweetypie_unmention_optimization_enabled": True,
                "vibe_api_enabled": True,
                "responsive_web_edit_tweet_api_enabled": True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                "view_counts_everywhere_api_enabled": True,
                "longform_notetweets_consumption_enabled": True,
                "tweet_awards_web_tipping_enabled": False,
                "freedom_of_speech_not_reach_fetch_enabled": False,
                "standardized_nudges_misinfo": True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
                "interactive_text_enabled": True,
                "responsive_web_text_conversations_enabled": False,
                "longform_notetweets_richtext_consumption_enabled": False,
                "responsive_web_enhance_cards_enabled": False
                })
            }


def get_timeline_endpoint_params(id: int):
    return {
            "variables": json.dumps({
                "userId": id,
                "count": 40,
                "includePromotedContent": True,
                "withCommunity": True,
                "withSuperFollowsUserFields": True,
                "withDownvotePerspective": False,
                "withReactionsMetadata": False,
                "withReactionsPerspective": False,
                "withSuperFollowsTweetFields": True,
                "withVoice": True,
                "withV2Timeline": False
                }),
            "features": json.dumps({
                "responsive_web_twitter_blue_verified_badge_is_enabled": True,
                "responsive_web_graphql_exclude_directive_enabled": True,
                "verified_phone_label_enabled": False,
                "responsive_web_graphql_timeline_navigation_enabled": True,
                "responsive_web_graphql_skip_user_profile_image_extensions_enabled": False,
                "tweetypie_unmention_optimization_enabled": True,
                "vibe_api_enabled": True,
                "responsive_web_edit_tweet_api_enabled": True,
                "graphql_is_translatable_rweb_tweet_is_translatable_enabled": True,
                "view_counts_everywhere_api_enabled": True,
                "longform_notetweets_consumption_enabled": True,
                "tweet_awards_web_tipping_enabled": False,
                "freedom_of_speech_not_reach_fetch_enabled": False,
                "standardized_nudges_misinfo": True,
                "tweet_with_visibility_results_prefer_gql_limited_actions_policy_enabled": False,
                "interactive_text_enabled": True,
                "responsive_web_text_conversations_enabled": False,
                "longform_notetweets_richtext_consumption_enabled": False,
                "responsive_web_enhance_cards_enabled": False,
                "creator_subscriptions_tweet_preview_api_enabled": True,
                "rweb_lists_timeline_redesign_enabled": True,
                "longform_notetweets_inline_media_enabled": True, 
                "responsive_web_twitter_article_tweet_consumption_enabled": False,
                "longform_notetweets_rich_text_read_enabled": True,
                "responsive_web_media_download_video_enabled": False
                })
            }


def get_tweets(name: str, replies: bool = False):
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
                user_to_id_endpoint,
                headers=headers,
                params=get_user_to_id_params(name)
                )
        if (user_id_response.status_code != 200):
            print("couldn't get user id")
            print(user_id_response.status_code)
            return
        user_id = json.loads(user_id_response.content)['data']['user']['result']['rest_id']
        timeline_response = requests.get(
                timeline_replies_endpoint if replies else timeline_endpoint,
                headers=headers,
                params=get_timeline_replies_endpoint_params(user_id) if replies else get_timeline_endpoint_params(user_id)
                )
        if (timeline_response.status_code != 200):
            print("couldn't get content")
            print(timeline_response.status_code)
            print(timeline_response.content)
            return
        timeline = json.loads(timeline_response.content)['data']['user']['result']['timeline']['timeline']['instructions']
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
                    quoted_parent = tweet['content']['itemContent']['tweet_results']['result']
                    if 'quoted_status_result' in quoted_parent:
                        quoted_parent = quoted_parent['quoted_status_result']
                    else:  # TODO: probably because of RT
                        quoted_parent = tweet_content['retweeted_status_result']
                    quoted = quoted_parent['result']['legacy']
                    quoted_author = quoted_parent['result']['core']['user_results']['result']['legacy']
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
