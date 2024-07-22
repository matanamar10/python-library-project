from mongoengine import connect, disconnect
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


# Define MongoDB settings class
class MongoDBSettings(BaseSettings):
    mongo_client: str
    mongo_db_name: str
    mongo_patrons_collection: str
    mongo_items_collection: str
    mongo_bills_collection: str

    class Config:
        env_file = '.env'


# Connect to MongoDB function
def connect_to_mongodb(settings):
    connect(db=settings.mongo_db_name, host=settings.mongo_client)


# Disconnect from MongoDB function
def disconnect_from_mongodb():
    disconnect()
