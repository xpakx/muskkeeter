from fastapi import FastAPI
from .downloader import get_tweets
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
