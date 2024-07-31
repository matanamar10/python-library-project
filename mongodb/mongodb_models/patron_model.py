# Define Patron document
from mongoengine import Document, StringField, DictField, DateTimeField
from src.env_utils import MongoDBSettings


class PatronDocument(Document):
    name = StringField(required=True, max_length=60)
    patron_id = StringField(required=True, unique=True, regex=r'^\d{9}$')
    patron_items = DictField(field=DateTimeField())

    meta = {
        'collection': MongoDBSettings().mongo_patrons_collection
    }
