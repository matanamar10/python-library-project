# mongodb_handler.py

from typing import Dict, Any, Optional, Union
from datetime import datetime
from mongodb.mongo_repository import MongoLibraryItemRepository, MongoPatronRepository, MongoBillRepository
from dal.dal import LibraryItemRepository, PatronRepository, BillRepository
from mongodb.mongodb_models.library_item_model import LibraryItemDocument
from mongodb.mongodb_models.patron_model import PatronDocument

# Instantiate the repository implementations
library_item_repo: LibraryItemRepository = MongoLibraryItemRepository()
patron_repo: PatronRepository = MongoPatronRepository()
bill_repo: BillRepository = MongoBillRepository()


def update_item_status(isbn: str, is_borrowed: bool) -> None:
    library_item_repo.update_item_status(isbn, is_borrowed)


def update_patron_items(patron_id: str, isbn: str, action: str, borrow_date: Optional[datetime] = None) -> None:
    patron_repo.update_patron_items(patron_id, isbn, action, borrow_date)


def insert_document(collection_name: str, document: Union[PatronDocument, LibraryItemDocument]):
    if collection_name == 'library-patrons':
        patron_repo.insert_document(collection_name, document)
    elif collection_name == 'library-items':
        library_item_repo.insert_document(collection_name, document)


def delete_document(collection_name: str, query: Dict[str, Any]) -> None:
    if collection_name == 'library-patrons':
        patron_repo.delete_document(query)
    elif collection_name == 'library-items':
        library_item_repo.delete_document(collection_name, query)


def insert_bill(patron_id: str, amount: float) -> None:
    bill_repo.insert_bill(patron_id, amount)


def update_bill(patron_id: str, amount: float) -> None:
    bill_repo.update_bill(patron_id, amount)


def delete_bill(patron_id: str) -> None:
    bill_repo.delete_bill(patron_id)
