from fastapi import FastAPI
from .downloader import get_tweets, get_tweets_and_replies
from .tweet_downloader import get_tweet
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/profile/{username}")
async def get_timeline(username: str):
    return get_tweets(username)


@app.get("/profile/{username}/replies")
async def get_timeline_with_replies(username: str):
    return get_tweets_and_replies(username)


@app.get("/tweet/{id}")
async def get_single_tweet(id: str):
    return get_tweet(id)
