from abc import ABC, abstractmethod
from typing import Optional, Dict, List
from datetime import datetime

from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument
from src.mongodb.mongodb_models.patron_model import PatronDocument


class LibraryItemRepository(ABC):
    @abstractmethod
    async def update_item_status(self, isbn: str, is_borrowed: bool) -> None:
        """
        Asynchronously update the status of a library item by its ISBN.

        Args:
            isbn (str): The ISBN of the library item.
            is_borrowed (bool): True if the item is borrowed, False if it is returned.
        """
        pass

    @abstractmethod
    async def insert_document(self, document: LibraryItemDocument) -> None:
        """
        Asynchronously insert a library item document into the database.

        Args:
            document (LibraryItemDocument): The document to insert.
        """
        pass

    @abstractmethod
    async def delete_document(self, query: dict) -> None:
        """
        Asynchronously delete a library item document from the database.

        Args:
            query (dict): The query to find the document to delete.
        """
        pass

    @abstractmethod
    async def item_exists(self, isbn: str) -> bool:
        """
        Asynchronously check if a library item exists by its ISBN.

        Args:
            isbn (str): The ISBN of the library item.

        Returns:
            bool: True if the item exists, False otherwise.
        """
        pass

    @abstractmethod
    async def is_item_borrowed(self, isbn: str) -> bool:
        """
        Asynchronously check if a library item is borrowed by its ISBN.

        Args:
            isbn (str): The ISBN of the library item.

        Returns:
            bool: True if the item is borrowed, False otherwise.
        """
        pass

    @abstractmethod
    async def search_items(self, query: Dict[str, Optional[str]]) -> List[LibraryItemDocument]:
        """
        Asynchronously search for library items based on a query.

        Args:
            query (Dict[str, Optional[str]]): Search criteria.

        Returns:
            List[LibraryItemDocument]: List of matching library items.
        """
        pass


class PatronRepository(ABC):
    @abstractmethod
    async def borrow_item(self, patron_id: str, isbn: str, borrow_date: Optional[datetime] = None):
        """
        Asynchronously borrow an item for a library patron.

        Args:
            patron_id (str): The ID of the patron.
            isbn (str): The ISBN of the item.
            borrow_date (Optional[datetime]): The date when the item is borrowed.
        """
        pass

    @abstractmethod
    async def return_item(self, patron_id: str, isbn: str):
        """
        Asynchronously return an item for a library patron.

        Args:
            patron_id (str): The ID of the patron.
            isbn (str): The ISBN of the item.
        """
        pass

    @abstractmethod
    async def insert_document(self, document: PatronDocument) -> None:
        """
        Asynchronously insert a patron document into the database.

        Args:
            document (PatronDocument): The document to insert.
        """
        pass

    @abstractmethod
    async def delete_document(self, query: dict) -> None:
        """
        Asynchronously delete a patron document from the database.

        Args:
            query (dict): The query to find the document to delete.
        """
        pass

    @abstractmethod
    async def patron_exists(self, patron_id: str) -> bool:
        """
        Asynchronously check if a patron exists by their ID.

        Args:
            patron_id (str): The ID of the patron.

        Returns:
            bool: True if the patron exists, False otherwise.
        """
        pass


class BillRepository(ABC):
    @abstractmethod
    async def insert_bill(self, patron_id: str, amount: float) -> None:
        """
        Asynchronously insert a new bill for a patron.

        Args:
            patron_id (str): The ID of the patron.
            amount (float): The amount of the bill.
        """
        pass

    @abstractmethod
    async def update_bill(self, patron_id: str, amount: float) -> None:
        """
        Asynchronously update the bill for a patron.

        Args:
            patron_id (str): The ID of the patron.
            amount (float): The new amount for the bill.
        """
        pass

    @abstractmethod
    async def delete_bill(self, patron_id: str) -> None:
        """
        Asynchronously delete the bill for a patron.

        Args:
            patron_id (str): The ID of the patron.
        """
        pass
