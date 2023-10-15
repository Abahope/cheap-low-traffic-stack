import datetime
from enum import Enum
from logging import getLogger

from aiobotocore.session import get_session
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from starlette import status
from mangum import Mangum

logger = getLogger(__name__)


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
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.get("/items")
async def get_items() -> dict[str, Item]:
    async with client() as db:
        # Get all the keys
        response = await db.scan(
            TableName=ItemsTable.name_.value,
            ProjectionExpression=ItemsTable.primary_key.value,
        )
        keys = [item[ItemsTable.primary_key.value]["S"] for item in response["Items"]]
        if not keys:
            return {}

        # Get all the items
        response = await db.batch_get_item(
            RequestItems={
                ItemsTable.name_.value: {
                    "Keys": [{ItemsTable.primary_key.value: {"S": key}} for key in keys]
                }
            }
        )
        return {
            item[ItemsTable.primary_key.value]["S"]: ItemsTable.deserializer(item)
            for item in response["Responses"][ItemsTable.name_.value]
        }


def handler(event, context):
    logger.debug(f"Received event {event}")
    magnum = Mangum(app)
    response = magnum(event, context)
    return response
