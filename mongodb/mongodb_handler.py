from typing import Union, Tuple
from mongodb.mongodb_models.bills_model import Bill
from mongodb.mongodb_models.patron_model import PatronDocument
from mongodb.mongodb_models.library_item_model import LibraryItemDocument


def update_item_status(isbn, is_borrowed):
    """
    Update the status of a library item identified by its ISBN.

    Args:
        isbn (str): The ISBN of the library item.
        is_borrowed (bool): True if the item is borrowed, False if it is returned.

    """
    library_item = LibraryItemDocument.objects.get(isbn=isbn)
    library_item.is_borrowed = is_borrowed
    library_item.save()


def update_patron_items(patron_id, isbn, action, borrow_date=None):
    """
    Update the items associated with a library patron.

    Args:
        patron_id (str): The ID of the patron.
        isbn (str): The ISBN of the library item.
        action (str): The action to perform ('borrow' or 'return').i
        borrow_date (str, optional): The date the item was borrowed (default is None).

    """
    patron = PatronDocument.objects.get(patron_id=patron_id)
    if action == "borrow":
        patron.patron_items[isbn] = borrow_date
    elif action == "return":
        if isbn in patron.patron_items:
            del patron.patron_items[isbn]
    patron.save()


def insert_document(collection_name, document: Union[PatronDocument, LibraryItemDocument]):
    """
    Insert a document into the specified MongoDB collection.

    Args:
        collection_name (str): The name of the MongoDB collection.
        document (Union[PatronDocument, LibraryItemDocument]): The document to insert into the collection.

    Returns:
        Tuple[bool, str]: A tuple indicating success (True) or failure (False), and an error message if applicable.
    """
    if collection_name == 'library-patrons':
        if PatronDocument.objects(patron_id=document.patron_id).first():
            return False, f"Patron with ID {document.patron_id} already exists."
        document.save()
    elif collection_name == 'library-items':
        if LibraryItemDocument.objects(isbn=document.isbn).first():
            return False, f"Library item with ISBN {document.isbn} already exists."
        document.save()


def delete_document(collection_name, query):
    """
    Delete documents from the specified MongoDB collection based on the query.

    Args:
        collection_name (str): The name of the MongoDB collection.
        query (dict): The query to match documents for deletion.

    """
    if collection_name == 'library-patrons':
        PatronDocument.objects(__raw__=query).delete()
    elif collection_name == 'library-items':
        LibraryItemDocument.objects(__raw__=query).delete()


def insert_bill(patron_id: str, amount: float):
    """
    Insert a new bill for a patron.

    Args:
        patron_id (str): The ID of the patron.
        amount (float): The bill amount.

    """
    bill = Bill(patron_id=patron_id, amount=amount)
    bill.save()


def update_bill(patron_id: str, amount: float):
    """
    Update the bill for a patron.

    Args:
        patron_id (str): The ID of the patron.
        amount (float): The new bill amount.
    """
    bill = Bill.objects.get(patron_id=patron_id)
    bill.amount = amount
    bill.save()


def delete_bill(patron_id: str):
    """
    Delete the bill for a patron.

    Args:
        patron_id (str): The ID of the patron.

    """
    Bill.objects.get(patron_id=patron_id).delete()
