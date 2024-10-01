from src.mongodb.mongodb_models.library_item_model import LibraryItem


class Disk(LibraryItem):
    disk_type: str
