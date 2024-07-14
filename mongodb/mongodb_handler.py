from typing import Union, Tuple
from mongoengine import DoesNotExist, MultipleObjectsReturned, NotUniqueError, ValidationError, OperationError
from mongodb.mongodb_models.bills_model import Bill
from mongodb.mongodb_models.patron_model import PatronDocument
from mongodb.mongodb_models.library_item_model import LibraryItemDocument


def update_item_status(isbn, is_borrowed) -> Tuple[bool, str]:
    """
    Update the status of a library item identified by its ISBN.

    Args:
        isbn (str): The ISBN of the library item.
        is_borrowed (bool): True if the item is borrowed, False if it is returned.

    Returns:
        Tuple[bool, str]: A tuple indicating success (True) or failure (False), and an error message if applicable.
    """
    try:
        library_item = LibraryItemDocument.objects.get(isbn=isbn)
        library_item.is_borrowed = is_borrowed
        library_item.save()
        return True, ""
    except DoesNotExist:
        return False, f"Library item with ISBN {isbn} does not exist."
    except MultipleObjectsReturned:
        return False, f"Multiple items found with ISBN {isbn}."
    except ValidationError as e:
        return False, f"Validation error: {e}"
    except OperationError as e:
        return False, f"Operation error: {e}"
    except Exception as e:
        return False, f"Update library item status failed: {e}"


def update_patron_items(patron_id, isbn, action, borrow_date=None) -> Tuple[bool, str]:
    """
    Update the items associated with a library patron.

    Args:
        patron_id (str): The ID of the patron.
        isbn (str): The ISBN of the library item.
        action (str): The action to perform ('borrow' or 'return').
        borrow_date (str, optional): The date the item was borrowed (default is None).

    Returns:
        Tuple[bool, str]: A tuple indicating success (True) or failure (False), and an error message if applicable.
    """
    try:
        patron = PatronDocument.objects.get(patron_id=patron_id)
        if action == "borrow":
            patron.patron_items[isbn] = borrow_date
        elif action == "return":
            if isbn in patron.patron_items:
                del patron.patron_items[isbn]
        patron.save()
        return True, ""
    except DoesNotExist:
        return False, f"Patron with ID {patron_id} does not exist."
    except MultipleObjectsReturned:
        return False, f"Multiple patrons found with ID {patron_id}."
    except ValidationError as e:
        return False, f"Validation error: {e}"
    except OperationError as e:
        return False, f"Operation error: {e}"
    except Exception as e:
        return False, f"Update library patron status failed: {e}"


def insert_document(collection_name, document: Union[PatronDocument, LibraryItemDocument]) -> Tuple[bool, str]:
    """
    Insert a document into the specified MongoDB collection.

    Args:
        collection_name (str): The name of the MongoDB collection.
        document (Union[PatronDocument, LibraryItemDocument]): The document to insert into the collection.

    Returns:
        Tuple[bool, str]: A tuple indicating success (True) or failure (False), and an error message if applicable.
    """
    try:
        if collection_name == 'library-patrons':
            if PatronDocument.objects(patron_id=document.patron_id).first():
                return False, f"Patron with ID {document.patron_id} already exists."
            document.save()
        elif collection_name == 'library-items':
            if LibraryItemDocument.objects(isbn=document.isbn).first():
                return False, f"Library item with ISBN {document.isbn} already exists."
            document.save()
        return True, ""
    except Exception as e:
        return False, str(e)


def delete_document(collection_name, query) -> Tuple[bool, str]:
    """
    Delete documents from the specified MongoDB collection based on the query.

    Args:
        collection_name (str): The name of the MongoDB collection.
        query (dict): The query to match documents for deletion.

    Returns:
        Tuple[bool, str]: A tuple indicating success (True) or failure (False), and an error message if applicable.
    """
    try:
        if collection_name == 'library-patrons':
            PatronDocument.objects(__raw__=query).delete()
        elif collection_name == 'library-items':
            LibraryItemDocument.objects(__raw__=query).delete()
        else:
            return False, f"Unknown collection: {collection_name}"
        return True, ""
    except DoesNotExist:
        return False, f"No documents found matching the query in {collection_name}."
    except ValidationError as e:
        return False, f"Validation error: {e}"
    except OperationError as e:
        return False, f"Operation error: {e}"
    except Exception as e:
        return False, f"Delete document failed: {e}"


def insert_bill(patron_id: str, amount: float) -> Tuple[bool, str]:
    """
    Insert a new bill for a patron.

    Args:
        patron_id (str): The ID of the patron.
        amount (float): The bill amount.

    Returns:
        Tuple[bool, str]: A tuple indicating success (True) or failure (False), and an error message if applicable.
    """
    try:
        bill = Bill(patron_id=patron_id, amount=amount)
        bill.save()
        return True, ""
    except NotUniqueError as e:
        return False, f"Bill for patron with ID {patron_id} already exists: {e}"
    except ValidationError as e:
        return False, f"Validation error: {e}"
    except OperationError as e:
        return False, f"Operation error: {e}"
    except Exception as e:
        return False, f"Insert bill failed: {e}"


def update_bill(patron_id: str, amount: float) -> Tuple[bool, str]:
    """
    Update the bill for a patron.

    Args:
        patron_id (str): The ID of the patron.
        amount (float): The new bill amount.

    Returns:
        Tuple[bool, str]: A tuple indicating success (True) or failure (False), and an error message if applicable.
    """
    try:
        bill = Bill.objects.get(patron_id=patron_id)
        bill.amount = amount
        bill.save()
        return True, ""
    except DoesNotExist:
        return insert_bill(patron_id, amount)
    except MultipleObjectsReturned:
        return False, f"Multiple bills found for patron with ID {patron_id}."
    except ValidationError as e:
        return False, f"Validation error: {e}"
    except OperationError as e:
        return False, f"Operation error: {e}"
    except Exception as e:
        return False, f"Update bill failed: {e}"


def delete_bill(patron_id: str) -> Tuple[bool, str]:
    """
    Delete the bill for a patron.

    Args:
        patron_id (str): The ID of the patron.

    Returns:
        Tuple[bool, str]: A tuple indicating success (True) or failure (False), and an error message if applicable.
    """
    try:
        Bill.objects.get(patron_id=patron_id).delete()
        return True, ""
    except DoesNotExist:
        return False, f"No bill found for patron with ID {patron_id}."
    except MultipleObjectsReturned:
        return False, f"Multiple bills found for patron with ID {patron_id}."
    except ValidationError as e:
        return False, f"Validation error: {e}"
    except OperationError as e:
        return False, f"Operation error: {e}"
    except Exception as e:
        return False, f"Delete bill failed: {e}"
