from mongodb.mongo_repository import MongoLibraryItemRepository, MongoPatronRepository, MongoBillRepository


class ControllersManager:
    def __init__(self):
        self.library_item_repo = MongoLibraryItemRepository()
        self.patron_repo = MongoPatronRepository()
        self.bill_repo = MongoBillRepository()

    def get_library_item_repo(self):
        return self.library_item_repo

    def get_patron_repo(self):
        return self.patron_repo

    def get_bill_repo(self):
        return self.bill_repo
