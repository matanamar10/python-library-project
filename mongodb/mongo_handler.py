# mongo_handler.py
from pymongo import MongoClient

MONGO_CLIENT = 'mongodb://localhost:27017/'
client = MongoClient(MONGO_CLIENT)
db = client.library
patrons_collection = db['library-patrons']
library_items_collection = db['library-items']
library_bills_collection = db['library-bills']


def update_item_status(isbn, is_borrowed):
    library_items_collection.update_one(
        {"isbn": isbn},
        {"$set": {"is_borrowed": is_borrowed}}
    )


def update_patron_items(patron_id, isbn, action, borrow_date=None):
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
    collection = db[collection_name]
    result = collection.insert_one(document)
    return result.inserted_id


def delete_document(collection_name, query):
    collection = db[collection_name]
    result = collection.delete_one(query)
    return result.deleted_count
