from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument
from src.mongodb.mongodb_models.patron_model import PatronDocument
from src.mongodb.mongodb_models.bills_model import BillDocument
from src.env_utils import MongoDBSettings


class MongoDBConnectionManager:

    def __init__(self):
        self.client: AsyncIOMotorClient = None

    async def connect(self):
        if self.client is not None:
            raise RuntimeError("MongoDB client is already connected.")

        self.client = AsyncIOMotorClient(MongoDBSettings().mongo_client)
        db = self.client[MongoDBSettings().mongo_db_name]
        await init_beanie(database=db, document_models=[LibraryItemDocument, PatronDocument, BillDocument])

    async def disconnect(self):
        if self.client is None:
            raise RuntimeError("MongoDB client is not initialized or already disconnected.")
        self.client.close()
        self.client = None
