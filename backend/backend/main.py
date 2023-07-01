from fastapi import FastAPI

app = FastAPI()


@app.get("/profile/{username}")
async def get_timeline(username: str):
    return None
