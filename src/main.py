import logging
from env_utils import MongoDBSettings
from mongodb.mongo_setup import connect_to_mongodb, disconnect_from_mongodb
from src.check_library import check_library
from utils.custom_library_errors import *


def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    try:
        settings = MongoDBSettings()
        connect_to_mongodb(settings)
        check_library()
    except LibraryError as e:
        logging.error(f"Library Item f: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise
    finally:
        disconnect_from_mongodb()


if __name__ == "__main__":
    main()
