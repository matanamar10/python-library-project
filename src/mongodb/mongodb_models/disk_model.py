from mongoengine import StringField

from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument


class DiskDocument(LibraryItemDocument):
    disk_type = StringField(required=True, max_length=60)
