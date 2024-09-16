from beanie import Document
from src.env_utils import MongoDBSettings


class BillDocument(Document):
    patron_id: str
    patron_bill_sum: float

    class Settings:
        collection = MongoDBSettings().mongo_bills_collection
