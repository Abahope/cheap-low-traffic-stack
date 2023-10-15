import datetime

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    """Use this route to warm the lambda and reduce cold starts."""
    return f"You are at the index page. The time is: {datetime.datetime.utcnow()}"
