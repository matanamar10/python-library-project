from mongoengine import Document, StringField, BooleanField

from mongodb.mongo_setup import settings


class LibraryItemDocument(Document):
    is_borrowed = BooleanField(default=False)
    title = StringField(required=True, max_length=60)
    isbn = StringField(required=True, unique=True, regex=r'^\d{9}$')
    type = StringField(required=True, choices=("Disk", "Book"))
    meta = {'allow_inheritance': True, 'collection': settings.mongo_items_collection}
