# dal.py

from abc import ABC, abstractmethod
from typing import Optional, Union
from datetime import datetime

from mongodb.mongodb_models.library_item_model import LibraryItemDocument
from mongodb.mongodb_models.patron_model import PatronDocument


class LibraryItemRepository(ABC):
    @abstractmethod
    def update_item_status(self, isbn: str, is_borrowed: bool):
        """Update the status of a library item by its ISBN."""
        pass

    @abstractmethod
    def insert_document(self, collection_name, document: Union[PatronDocument, LibraryItemDocument]):
        """Insert a library item document."""
        pass

    @abstractmethod
    def delete_document(self, collection_name, query):
        """Delete a library item document."""
        pass


class PatronRepository(ABC):
    @abstractmethod
    def update_patron_items(self, patron_id: str, isbn: str, action: str,
                            borrow_date: Optional[datetime] = None):
        """Update the items associated with a library patron."""
        pass

    @abstractmethod
    def insert_document(self, collection_name, document: Union[PatronDocument, LibraryItemDocument]):
        """Insert a patron document."""

    pass

    @abstractmethod
    def delete_document(self, query):
        """Delete a patron document."""
        pass


class BillRepository(ABC):
    @abstractmethod
    def insert_bill(self, patron_id: str, amount: float):
        """Insert a new bill for a patron."""
        pass

    @abstractmethod
    def update_bill(self, patron_id: str, amount: float):
        """Update the bill for a patron."""
        pass

    @abstractmethod
    def delete_bill(self, patron_id: str):
        """Delete the bill for a patron."""
        pass
