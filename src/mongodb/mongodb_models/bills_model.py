from beanie import Document
from pydantic import Field
from src.env_utils import MongoDBSettings


class BillDocument(Document):
    patron_id: str = Field(..., regex=r'^\d{9}$', unique=True)
    patron_bill_sum: float = Field(...)

    class Settings:
        collection = MongoDBSettings().mongo_bills_collection  # Ensure this matches your collection name
