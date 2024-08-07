# mongodb/mongo_repository.py

from typing import Dict, Any, Optional
from datetime import datetime
from dal.dal import LibraryItemRepository, PatronRepository, BillRepository
from mongodb.mongodb_models.library_item_model import LibraryItemDocument
from mongodb.mongodb_models.patron_model import PatronDocument
from mongodb.mongodb_models.bills_model import Bill


class MongoLibraryItemRepository(LibraryItemRepository):
    def update_item_status(self, isbn: str, is_borrowed: bool) -> None:
        """
        Update the status of a library item identified by its ISBN.

        Args:
            isbn (str): The ISBN of the library item.
            is_borrowed (bool): True if the item is borrowed, False if it is returned.
        """
        item = LibraryItemDocument.objects(isbn=isbn).first()
        if item:
            item.update(set__is_borrowed=is_borrowed)

    def insert_document(self, document: LibraryItemDocument) -> None:
        """
        Insert a library item document into the database.

        Args:
            document (LibraryItemDocument): The document to insert.
        """
        document.save()

    def delete_document(self, query: Dict[str, Any]) -> None:
        """
        Delete a library item document from the database.

        Args:
            query (dict): The query to find the document to delete.
        """
        LibraryItemDocument.objects(**query).delete()


class MongoPatronRepository(PatronRepository):
    def return_item(self, patron_id: str, isbn: str):
        """
        Update the items associated with a library patron.

        Args:
            patron_id (str): The ID of the patron.
            isbn (str): The ISBN of the item.
        """
        patron = PatronDocument.objects(patron_id=patron_id).first()
        patron.patron_items.pop(isbn, None)
        patron.save()

    def borrow_item(self, patron_id: str, isbn: str, borrow_date: Optional[datetime] = None):
        """
        Update the items associated with a library patron.

        Args:
            patron_id (str): The ID of the patron.
            isbn (str): The ISBN of the item.
            borrow_date (Optional[datetime]): The date when the item is borrowed.
        """

        patron = PatronDocument.objects(patron_id=patron_id).first()
        patron.patron_items[isbn] = borrow_date
        patron.save()

    def insert_document(self, document: PatronDocument) -> None:
        """
        Insert a patron document into the database.

        Args:
            document (PatronDocument): The document to insert.
        """
        document.save()

    def delete_document(self, query: Dict[str, Any]) -> None:
        """
        Delete a patron document from the database.

        Args:
            query (dict): The query to find the document to delete.
        """
        PatronDocument.objects(**query).delete()


class MongoBillRepository(BillRepository):
    def insert_bill(self, patron_id: str, amount: float) -> None:
        """
        Insert a new bill for a patron.

        Args:
            patron_id (str): The ID of the patron.
            amount (float): The amount of the bill.
        """
        bill = Bill(patron_id=patron_id, amount=amount)
        bill.save()

    def update_bill(self, patron_id: str, amount: float) -> None:
        """
        Update the bill for a patron.

        Args:
            patron_id (str): The ID of the patron.
            amount (float): The new amount for the bill.
        """
        bill = Bill.objects(patron_id=patron_id).first()
        if bill:
            bill.update(set__amount=amount)

    def delete_bill(self, patron_id: str) -> None:
        """
        Delete the bill for a patron.

        Args:
            patron_id (str): The ID of the patron.
        """
        Bill.objects(patron_id=patron_id).delete()
