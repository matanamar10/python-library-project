from pydantic_settings import BaseSettings


# Define MongoDB settings class
class MongoDBSettings(BaseSettings):
    mongo_client: str
    mongo_db_name: str
    mongo_patrons_collection: str
    mongo_items_collection: str
    mongo_bills_collection: str

    class Config:
        env_file = '.env'
