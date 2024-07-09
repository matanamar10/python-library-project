from mongodb.mongodb_handler import (
    update_item_status,
    update_patron_items,
    insert_document,
    delete_document, delete_bill, update_bill, insert_bill
)


def update_item_dal(isbn, is_borrowed):
    """
    Update the status of a library item identified by its ISBN.

    Args:
        isbn (str): The ISBN of the library item.
        is_borrowed (bool): True if the item is borrowed, False if it is returned.

    Raises:
        Exception: If updating the library item status fails.
    """
    try:
        update_item_status(isbn, is_borrowed)
    except Exception as e:
        raise Exception(f"Update library item status failed: {e}")


def update_patron_dal(patron_id, isbn, action, borrow_date=None):
    """
    Update the status of a library patron's items based on the action specified.

    Args:
        patron_id (str): The ID of the patron.
        isbn (str): The ISBN of the library item.
        action (str): The action to perform ('borrow' or 'return').
        borrow_date (datetime, optional): The date the item was borrowed (default is None).

    Raises:
        Exception: If updating the library patron status fails.
    """
    try:
        update_patron_items(patron_id, isbn, action, borrow_date)
    except Exception as e:
        raise Exception(f"Update library patron status failed: {e}")


def insert_document_dal(collection_name, document):
    """
    Insert a document into the specified MongoDB collection.

    Args:
        document (Document): The document to insert into the collection.

    Returns:
        str: The ID of the inserted document.

    Raises:
        Exception: If inserting the document fails.
        :param document:
        :param collection_name:
    """
    try:
        return insert_document(collection_name, document)
    except Exception as e:
        raise Exception(f"Insert document failed: {e}")


def delete_document_dal(collection_name, query):
    """
    Delete documents from the specified MongoDB collection based on the query.

    Args:
        collection_name (str): The name of the MongoDB collection.
        query (dict): The query to match documents for deletion.

    Raises:
        Exception: If deleting documents fails.
    """
    try:
        delete_document(collection_name, query)
    except Exception as e:
        raise Exception(f"Delete document failed: {e}")


def insert_bill_dal(patron_id, amount):
    """
    Insert a new bill for a patron.

    Args:
        patron_id (str): The ID of the patron.
        amount (float): The bill amount.

    Raises:
        Exception: If inserting the bill fails.
    """
    try:
        insert_bill(patron_id, amount)
    except Exception as e:
        raise Exception(f"Insert bill failed: {e}")


def update_bill_dal(patron_id, amount):
    """
    Update the bill for a patron.

    Args:
        patron_id (str): The ID of the patron.
        amount (float): The new bill amount.

    Raises:
        Exception: If updating the bill fails.
    """
    try:
        update_bill(patron_id, amount)
    except Exception as e:
        raise Exception(f"Update bill failed: {e}")


def delete_bill_dal(patron_id):
    """
    Delete the bill for a patron.

    Args:
        patron_id (str): The ID of the patron.

    Raises:
        Exception: If deleting the bill fails.
    """
    try:
        delete_bill(patron_id)
    except Exception as e:
        raise Exception(f"Delete bill failed: {e}")
