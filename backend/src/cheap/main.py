import datetime
from enum import Enum

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    id: str
    description: str


class ItemsTable(Enum):
    """A lighweight facade for the DynamoDB items table."""

    name_ = "items"
    primary_key = "id"

    @staticmethod
    def deserializer(item) -> Item:
        return Item(
            id=item["id"]["S"],
            description=item["description"]["S"],
        )


app = FastAPI()


@app.get("/")
async def root():
    """Use this route to warm the lambda and reduce cold starts."""
    return f"You are at the index page. The time is: {datetime.datetime.utcnow()}"
