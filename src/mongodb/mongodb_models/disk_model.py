from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument


class Disk(LibraryItemDocument):
    disk_type: str
