from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument
from src.mongodb.mongodb_models.patron_model import PatronDocument
from src.mongodb.mongodb_models.bills_model import BillDocument
from src.env_utils import MongoDBSettings

async def connect_to_mongodb():
    client = AsyncIOMotorClient(MongoDBSettings().mongo_client)
    db = client[MongoDBSettings().mongo_db_name]
    await init_beanie(database=db, document_models=[LibraryItemDocument, PatronDocument, BillDocument])

async def disconnect_from_mongodb():
    await AsyncIOMotorClient().close()
