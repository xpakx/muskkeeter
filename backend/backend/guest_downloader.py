import requests
import json
from datetime import datetime

android_api_key = ("CjulERsDeqhhjSme66ECg", "IQWdVyqFxghAtURHGeGiWAsmCAGmdW3WmbEx6Hck")
get_token_endpoint = "https://api.twitter.com/oauth2/token?grant_type=client_credentials"


def get_tweets(name: str):
    resp = requests.post(get_token_endpoint, auth=android_api_key)
    if (resp.status_code == 200):
        token = json.loads(resp.content)["access_token"]
        return {"token": token}
    else:
        print("failed")
