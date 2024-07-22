import logging

from mongodb.mongo_setup import connect_to_mongodb, disconnect_from_mongodb, MongoDBSettings
from utils.custom_errors import *


def main():
    try:
        settings = MongoDBSettings()
        connect_to_mongodb(settings)
    except LibraryError as e:
        logging.error(f"Library Error: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise
    finally:
        disconnect_from_mongodb()


if __name__ == "__main__":
    main()
