# mongo_handler.py

import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGO_CLIENT = os.getenv('MONGO_CLIENT')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME')
MONGO_PATRONS_COLLECTION = os.getenv('MONGO_PATRONS_COLLECTION')
MONGO_ITEMS_COLLECTION = os.getenv('MONGO_ITEMS_COLLECTION')
MONGO_BILLS_COLLECTION = os.getenv('MONGO_BILLS_COLLECTION')

# MongoDB client setup
client = MongoClient(MONGO_CLIENT)
db = client[MONGO_DB_NAME]
patrons_collection = db[MONGO_PATRONS_COLLECTION]
library_items_collection = db[MONGO_ITEMS_COLLECTION]
library_bills_collection = db[MONGO_BILLS_COLLECTION]


def update_item_status(isbn, is_borrowed):
    """
    Update the status of a library item identified by its ISBN.

    Args:
        isbn (str): The ISBN of the library item.
        is_borrowed (bool): True if the item is borrowed, False if it is returned.

    """
    library_items_collection.update_one(
        {"isbn": isbn},
        {"$set": {"is_borrowed": is_borrowed}}
    )


def update_patron_items(patron_id, isbn, action, borrow_date=None):
    """
    Update the items associated with a library patron.

    Args:
        patron_id (str): The ID of the patron.
        isbn (str): The ISBN of the library item.
        action (str): The action to perform ('borrow' or 'return').
        borrow_date (str, optional): The date the item was borrowed (default is None).

    """
    if action == "borrow":
        patrons_collection.update_one(
            {"patron_id": patron_id},
            {"$set": {f"patron_items.{isbn}": borrow_date}}
        )
    elif action == "return":
        patrons_collection.update_one(
            {"patron_id": patron_id},
            {"$unset": {f"patron_items.{isbn}": ""}}
        )


def insert_document(collection_name, document):
    """
    Insert a document into the specified MongoDB collection.

    Args:
        collection_name (str): The name of the MongoDB collection.
        document (dict): The document to insert into the collection.

    Returns:
        str: The ID of the inserted document.

    """
    collection = db[collection_name]
    result = collection.insert_one(document)
    return result.inserted_id


def delete_document(collection_name, query):
    """
    Delete documents from the specified MongoDB collection based on the query.

    Args:
        collection_name (str): The name of the MongoDB collection.
        query (dict): The query to match documents for deletion.

    Returns:
        int: The number of documents deleted.

    """
    collection = db[collection_name]
    result = collection.delete_one(query)
    return result.deleted_count
