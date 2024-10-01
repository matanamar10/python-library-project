from pydantic_settings import BaseSettings

class MongoDBSettings(BaseSettings):
    mongo_client: str
    mongo_db_name: str
    mongo_patrons_collection: str
    mongo_items_collection: str
    mongo_bills_collection: str

    class Config:
        env_file = '.env'

class MainSettings(BaseSettings):
    library_name: str
    host: str
    port: int

    class Config:
        env_file = ".env"