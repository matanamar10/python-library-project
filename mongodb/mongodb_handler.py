# mongodb/mongodb_handler.py
from typing import Union
from mongodb.mongodb_models.patron_model import PatronDocument
from mongodb.mongodb_models.library_item_model import LibraryItemDocument


def update_item_status(isbn, is_borrowed):
    """
    Update the status of a library item identified by its ISBN.

    Args:
        isbn (str): The ISBN of the library item.
        is_borrowed (bool): True if the item is borrowed, False if it is returned.
    """
    try:
        library_item = LibraryItemDocument.objects(isbn=isbn).first()
        if library_item:
            library_item.is_borrowed = is_borrowed
            library_item.save()
    except Exception as e:
        raise Exception(f"Update library item status failed: {e}")


def update_patron_items(patron_id, isbn, action, borrow_date=None):
    """
    Update the items associated with a library patron.

    Args:
        patron_id (str): The ID of the patron.
        isbn (str): The ISBN of the library item.
        action (str): The action to perform ('borrow' or 'return').
        borrow_date (str, optional): The date the item was borrowed (default is None).
    """
    try:
        patron = PatronDocument.objects(patron_id=patron_id).first()
        if patron:
            if action == "borrow":
                patron.patron_items[isbn] = borrow_date
            elif action == "return":
                if isbn in patron.patron_items:
                    del patron.patron_items[isbn]
            patron.save()
    except Exception as e:
        raise Exception(f"Update library patron status failed: {e}")


def insert_document(collection_name, document: Union[PatronDocument, LibraryItemDocument]):
    """
    Insert a document into the specified MongoDB collection.

    Args:
        collection_name (str): The name of the MongoDB collection.
        document (dict): The document to insert into the collection.
    """
    try:
        if collection_name == 'library-patrons':
            # Ensure patron_id is unique in library-patrons collection
            if PatronDocument.objects(patron_id=document.patron_id).first():
                raise Exception(f"Patron with id {document.patron_id} already exists.")
            document.save()
        elif collection_name == 'library-items':
            # Ensure isbn is unique in library-items collection
            if LibraryItemDocument.objects(isbn=document.isbn).first():
                raise Exception(f"Library item with ISBN {document.isbn} already exists.")
            document.save()
        else:
            raise Exception(f"Unknown collection: {collection_name}")
    except Exception as e:
        raise Exception(f"Insert document failed: {e}")


def delete_document(collection_name, query):
    """
    Delete documents from the specified MongoDB collection based on the query.

    Args:
        collection_name (str): The name of the MongoDB collection.
        query (dict): The query to match documents for deletion.
    """
    try:
        if collection_name == 'library-patrons':
            PatronDocument.objects(__raw__=query).delete()
        elif collection_name == 'library-items':
            LibraryItemDocument.objects(__raw__=query).delete()
    except Exception as e:
        raise Exception(f"Delete document failed: {e}")
