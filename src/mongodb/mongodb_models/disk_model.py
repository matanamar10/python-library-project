from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument


class DiskDocument(LibraryItemDocument):
    disk_type: str
