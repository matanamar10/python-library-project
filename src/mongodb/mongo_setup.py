from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument
from src.mongodb.mongodb_models.patron_model import PatronDocument
from src.mongodb.mongodb_models.bills_model import BillDocument
from src.env_utils import MongoDBSettings

client: AsyncIOMotorClient


async def connect_to_mongodb():
    global client
    if client is not None:
        raise RuntimeError("MongoDB client is already connected.")

    client = AsyncIOMotorClient(MongoDBSettings().mongo_client)
    db = client[MongoDBSettings().mongo_db_name]
    await init_beanie(database=db, document_models=[LibraryItemDocument, PatronDocument, BillDocument])


async def disconnect_from_mongodb():
    global client
    if client is None:
        raise RuntimeError("MongoDB client is not initialized or already disconnected.")
    client.close()  # Close the client connection (sync method)
    client = None  # Optionally set client to None after closing
