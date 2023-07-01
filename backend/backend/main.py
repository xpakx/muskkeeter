from fastapi import FastAPI
from .downloader import get_tweets

app = FastAPI()


@app.get("/profile/{username}")
async def get_timeline(username: str):
    return get_tweets(username)
