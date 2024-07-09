# Define Patron document
from mongoengine import Document, StringField, ReferenceField, DictField, DateTimeField

from mongodb.mongo_setup import settings


class PatronDocument(Document):
    name = StringField(required=True, max_length=60)
    patron_id = StringField(required=True, unique=True, regex=r'^\d{9}$')
    patron_items = DictField(field=DateTimeField())

    meta = {
        'collection': settings.mongo_patrons_collection
    }
