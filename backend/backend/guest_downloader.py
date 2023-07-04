import requests
import json

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

        return timeline
    else:
        print("failed")
