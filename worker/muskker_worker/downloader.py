import requests
from bs4 import BeautifulSoup

subscriptions = ["ed_hagen"]

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


def get_profile(name: str):
    url = f"https://syndication.twitter.com/srv/timeline-profile/screen-name/{name}"
    html = requests.get(url, headers=headers).content
    soup = BeautifulSoup(html, "html.parser")
    data = soup.find("script", {"id": "__NEXT_DATA__"})
    if data:
        return data.text
    return None
