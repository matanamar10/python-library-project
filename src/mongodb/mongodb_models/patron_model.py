# Define Patron document
from beanie import Document
from mongoengine import StringField, DictField, DateTimeField

from src.env_utils import MongoDBSettings


class PatronDocument(Document):
    name = StringField(required=True, max_length=60)
    id = StringField(required=True, unique=True, regex=r'^\d{9}$')
    items = DictField(field=DateTimeField())

    meta = {
        'collection': MongoDBSettings().mongo_patrons_collection
    }
