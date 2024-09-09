from mongoengine import StringField
from pydantic import Field

from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument


class DiskDocument(LibraryItemDocument):
    disk_type: str = Field(..., max_length=60)
