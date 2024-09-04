# dal/dal.py

from abc import ABC, abstractmethod
from typing import Optional
from datetime import datetime

from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument
from src.mongodb.mongodb_models.patron_model import PatronDocument


class LibraryItemRepository(ABC):
    @abstractmethod
    def update_item_status(self, isbn: str, is_borrowed: bool) -> None:
        """
        Update the status of a library item by its ISBN.

        Args:
            isbn (str): The ISBN of the library item.
            is_borrowed (bool): True if the item is borrowed, False if it is returned.
        """
        pass

    @abstractmethod
    def insert_document(self, document: LibraryItemDocument) -> None:
        """
        Insert a library item document into the database.

        Args:
            document (LibraryItemDocument): The document to insert.
        """
        pass

    @abstractmethod
    def delete_document(self, query: dict) -> None:
        """
        Delete a library item document from the database.

        Args:
            query (dict): The query to find the document to delete.
        """
        pass

    @abstractmethod
    def item_exists(self, isbn: str) -> bool:
        """
        Check if a library item exists by its ISBN.

        Args:
            isbn (str): The ISBN of the library item.

        Returns:
            bool: True if the item exists, False otherwise.
        """
        pass

    def is_item_borrowed(self, isbn: str) -> bool:
        pass


class PatronRepository(ABC):
    @abstractmethod
    def borrow_item(self, patron_id: str, isbn: str, borrow_date: Optional[datetime] = None):
        """
        Borrow an item for a library patron.

        Args:
            patron_id (str): The ID of the patron.
            isbn (str): The ISBN of the item.
            borrow_date (Optional[datetime]): The date when the item is borrowed.
        """
        pass

    @abstractmethod
    def return_item(self, patron_id: str, isbn: str):
        """
        Return an item for a library patron.

        Args:
            patron_id (str): The ID of the patron.
            isbn (str): The ISBN of the item.
        """
        pass

    @abstractmethod
    def insert_document(self, document: PatronDocument) -> None:
        """
        Insert a patron document into the database.

        Args:
            document (PatronDocument): The document to insert.
        """
        pass

    @abstractmethod
    def delete_document(self, query: dict) -> None:
        """
        Delete a patron document from the database.

        Args:
            query (dict): The query to find the document to delete.
        """
        pass

    @abstractmethod
    def patron_exists(self, patron_id: str) -> bool:
        pass


class BillRepository(ABC):
    @abstractmethod
    def insert_bill(self, patron_id: str, amount: float) -> None:
        """
        Insert a new bill for a patron.

        Args:
            patron_id (str): The ID of the patron.
            amount (float): The amount of the bill.
        """
        pass

    @abstractmethod
    def update_bill(self, patron_id: str, amount: float) -> None:
        """
        Update the bill for a patron.

        Args:
            patron_id (str): The ID of the patron.
            amount (float): The new amount for the bill.
        """
        pass

    @abstractmethod
    def delete_bill(self, patron_id: str) -> None:
        """
        Delete the bill for a patron.

        Args:
            patron_id (str): The ID of the patron.
        """
        pass
