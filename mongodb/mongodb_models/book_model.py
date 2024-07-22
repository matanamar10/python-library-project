from mongoengine import StringField

from mongodb.mongodb_models.library_item_model import LibraryItemDocument


class BookDocument(LibraryItemDocument):
    author = StringField(required=True, max_length=60)
