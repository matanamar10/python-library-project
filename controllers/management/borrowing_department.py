import logging
from datetime import datetime
from mongoengine import DoesNotExist, MultipleObjectsReturned, ValidationError, OperationError
from controllers.management.finance import calculate_bill
from controllers.library import Library
from models.library_items.items import LibraryItem
from dal.dal import update_item_dal, update_patron_dal, update_bill_dal, delete_bill_dal


def return_a_library_item(library: Library, library_item: LibraryItem, patron_id: str):
    """
    Handles the return process of a library item by a patron.

    This function updates the library system when a patron returns a borrowed item. It checks if the patron
    exists, verifies if the item is in the library's inventory and currently borrowed, calculates any
    outstanding bills, and processes the return if all conditions are met.

    Parameters:
    - library (Library): The Library object representing the library system.
    - library_item (LibraryItem): The LibraryItem object (book, disk, etc.) being returned.
    - patron_id (str): The unique identifier for the patron returning the item.

    Raises:
    - ValueError: If the patron does not exist, the item is not in the library, the item is not borrowed,
                  or if the patron has outstanding bills.
    """
    try:
        patron = library.patrons.get(patron_id)
        if not patron:
            raise DoesNotExist(f"Patron with patron id {patron_id} was not found in the library")
        if library_item.isbn not in library.library_items.keys():
            raise DoesNotExist(f"The library item with ISBN {library_item.isbn} was not found in the library")
        if not library_item.is_borrowed:
            raise ValueError(f"Library item with ISBN {library_item.isbn} is not borrowed")

        patron_calculated_bill = calculate_bill(patron=patron)
        library.bills[patron_id] = patron_calculated_bill

        if library.bills[patron_id] != 0:
            update_bill_dal(patron_id, patron_calculated_bill)
            raise ValueError(f"Patron {patron_id} needs to pay their bill before returning library items")
        patron.remove_library_item_from_patron(library_item)
        library_item.is_borrowed = False  # The book is not borrowed anymore.
        update_patron_dal(patron_id, library_item.isbn, "return")
        update_item_dal(library_item.isbn, False)

        logging.info(f"Library item {library_item.title} has been returned by patron {patron_id}")

    except DoesNotExist as e:
        logging.error(f"Failed to return library item: {e}")
        raise ValueError(e)
    except MultipleObjectsReturned as e:
        logging.error(f"Multiple records found: {e}")
        raise ValueError(f"Multiple records found: {e}")
    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        raise ValueError(f"Validation error: {e}")
    except OperationError as e:
        logging.error(f"Database operation error: {e}")
        raise ValueError(f"Database operation error: {e}")
    except Exception as e:
        logging.error(f"Failed to return library item: {e}")
        raise ValueError(f"Failed to return library item: {e}")


def borrow_a_library_item(library: Library, library_item: LibraryItem, patron_id: str):
    """
    Handles the borrowing process of a library item by a patron.

    This function updates the library system when a patron borrows an item. It checks if the patron exists,
    verifies if the item is in the library's inventory and not currently borrowed, and processes the borrowing
    if all conditions are met.

    Parameters:
    - library (Library): The Library object representing the library system.
    - library_item (LibraryItem): The LibraryItem object (book, disk, etc.) being borrowed.
    - patron_id (str): The unique identifier for the patron borrowing the item.

    Raises:
    - ValueError: If the patron does not exist, the item is not in the library, or if the item is already borrowed.
    """
    try:
        if patron_id not in library.patrons.keys():
            raise DoesNotExist(f"Patron with ID {patron_id} not found in the library")
        if library_item.isbn not in library.library_items.keys():
            raise DoesNotExist(f"Library item with ISBN {library_item.isbn} not found in the library")
        if library_item.is_borrowed:
            raise ValueError(f"Library item with ISBN {library_item.isbn} is already borrowed")

        patron = library.patrons[patron_id]
        patron.add_library_item_to_patron(library_item=library_item)
        library_item.is_borrowed = True
        borrow_date = datetime.now()
        update_patron_dal(patron_id, library_item.isbn, "borrow", borrow_date)
        update_item_dal(library_item.isbn, True)

        logging.info(f"Library item {library_item.title} has been borrowed by patron {patron_id}")

    except DoesNotExist as e:
        logging.error(f"Failed to borrow library item: {e}")
        raise ValueError(e)
    except MultipleObjectsReturned as e:
        logging.error(f"Multiple records found: {e}")
        raise ValueError(f"Multiple records found: {e}")
    except ValidationError as e:
        logging.error(f"Validation error: {e}")
        raise ValueError(f"Validation error: {e}")
    except OperationError as e:
        logging.error(f"Database operation error: {e}")
        raise ValueError(f"Database operation error: {e}")
    except Exception as e:
        logging.error(f"Failed to borrow library item: {e}")
        raise ValueError(f"Failed to borrow library item: {e}")
