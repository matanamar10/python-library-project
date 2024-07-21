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

    """
    update_item_status(isbn, is_borrowed)


def update_patron_dal(patron_id, isbn, action, borrow_date=None):
    """
    Update the status of a library patron's items based on the action specified.

    Args:
        patron_id (str): The ID of the patron.
        isbn (str): The ISBN of the library item.
        action (str): The action to perform ('borrow' or 'return').
        borrow_date (datetime, optional): The date the item was borrowed (default is None).

    """
    update_patron_items(patron_id, isbn, action, borrow_date)


def insert_document_dal(collection_name, document):
    """
    Insert a document into the specified MongoDB collection.

    Args:
        document (Document): The document to insert into the collection.

    Returns:
        str: The ID of the inserted document.
        :param document:
        :param collection_name:

    """
    insert_document(collection_name, document)


def delete_document_dal(collection_name, query):
    """
    Delete documents from the specified MongoDB collection based on the query.

    Args:
        collection_name (str): The name of the MongoDB collection.
        query (dict): The query to match documents for deletion.

    """
    delete_document(collection_name, query)


def insert_bill_dal(patron_id, amount):
    """
    Insert a new bill for a patron.

    Args:
        patron_id (str): The ID of the patron.
        amount (float): The bill amount.

    """
    insert_bill(patron_id, amount)


def update_bill_dal(patron_id, amount):
    """
    Update the bill for a patron.

    Args:
        patron_id (str): The ID of the patron.
        amount (float): The new bill amount.

    """
    update_bill(patron_id, amount)


def delete_bill_dal(patron_id):
    """
    Delete the bill for a patron.

    Args:
        patron_id (str): The ID of the patron.
    """
    delete_bill(patron_id)
