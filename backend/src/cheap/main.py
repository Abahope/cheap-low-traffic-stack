import datetime
from enum import Enum

from aiobotocore.session import get_session
from fastapi import FastAPI
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from starlette import status


def client():
    return get_session().create_client("dynamodb", region_name="us-east-1")


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


@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item) -> Item:
    async with client() as db:
        # Check if the item already exists
        response = await db.get_item(
            TableName=ItemsTable.name_.value,
            Key={ItemsTable.primary_key.value: {"S": item.id}},
        )
        if "Item" in response:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Item with id {item.id} already exists.",
            )
        # Create the item
        await db.put_item(
            TableName=ItemsTable.name_.value,
            Item={
                ItemsTable.primary_key.value: {"S": item.id},
                "description": {"S": item.description},
            },
        )
        return item
