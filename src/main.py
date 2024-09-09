from src.app import create_app
from src.env_utils import MongoDBSettings
from src.mongodb.mongo_setup import connect_to_mongodb, disconnect_from_mongodb
from utils.custom_library_errors import *
import uvicorn


def main():
    try:
        settings = MongoDBSettings()
        connect_to_mongodb(settings)
        app = create_app(library_name="AmarLibrary")
        uvicorn.run(app, host="127.0.0.1", port=8000)
    except LibraryError as e:
        raise
    except Exception as e:
        raise
    finally:
        disconnect_from_mongodb()


if __name__ == "__main__":
    main()
