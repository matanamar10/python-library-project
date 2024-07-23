from mongoengine import Document, StringField, BooleanField
from env_utils import MongoDBSettings


class LibraryItemDocument(Document):
    is_borrowed = BooleanField(default=False)
    title = StringField(required=True, max_length=60)
    isbn = StringField(required=True, unique=True, regex=r'^\d{9}$')
    type = StringField(required=True, choices=("Disk", "Book"))
    meta = {'allow_inheritance': True, 'collection': MongoDBSettings().mongo_items_collection}
