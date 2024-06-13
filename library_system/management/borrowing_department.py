import logging
from exporter.export_data_to_excel import export_data, item_row_preparer
from library_system.management.finance import calculate_bill
from library_system.library import Library
from library_system.library_items.items import LibraryItem


def return_a_library_item(library: Library, library_item: LibraryItem, patron_id: str):
    """
    Handles the return process of a library_system item by a patron.

    This function updates the library_system system when a patron returns a borrowed item. It checks if the patron
    exists, verifies if the item is in the library_system's inventory and currently borrowed, calculates any
    outstanding bills, and processes the return if all conditions are met.

    Parameters:
    - library_system (Library): The Library object representing the library_system system.
    - library_item (LibraryItem): The LibraryItem object (book, disk, etc.) being returned.
    - patron_id (str): The unique identifier for the patron returning the item.

    Raises:
    - ValueError: If the patron does not exist, the item is not in the library_system, the item is not borrowed,
                  or if the patron has outstanding bills.
    """

    try:
        patron = library.patrons[patron_id]
        if not patron:
            raise ValueError(f"Patron with patron id {patron_id} was not found in the library_system")
        if library_item.isbn not in library.library_items.keys():
            raise ValueError(
                f"The library_system item with isbn {library_item.isbn} was not found in the library_system")
        if not library_item.is_borrowed:
            raise ValueError(f"Library item with ISBN {library_item.isbn} is not borrowed")
        patron_calculated_bill = calculate_bill(patron=patron)
        library.bills[patron_id] = patron_calculated_bill
        if library.bills[patron_id] != 0:
            raise ValueError(f"Patron {patron_id} needs to pay their bill before returning library_items")
        patron.remove_library_item_from_patron(library_item)
        library_item.is_borrowed = False  # The book is not borrowed anymore.
        # Call these functions from outside with all necessary parameters
        export_data(library.library_items, '../data/library_items.csv', ["ISBN", "Type", "Title", "Is Borrowed?"],
                    item_row_preparer)
        logging.info(f"Library item {library_item.title} has been returned by patron {patron_id}")
    except ValueError as e:
        logging.error(f"Failed to return library_system item: {e}")


def borrow_a_library_item(library: Library, library_item: LibraryItem, patron_id: str):
    """
    Handles the borrowing process of a library_system item by a patron.

    This function updates the library_system system when a patron borrows an item. It checks if the patron exists,
    verifies if the item is in the library_system's inventory and not currently borrowed, and processes the borrowing
    if all conditions are met.

    Parameters:
    - library_system (Library): The Library object representing the library_system system.
    - library_item (LibraryItem): The LibraryItem object (book, disk, etc.) being borrowed.
    - patron_id (str): The unique identifier for the patron borrowing the item.

    Raises:
    - ValueError: If the patron does not exist, the item is not in the library_system, or if the item is already borrowed.
    """

    try:
        patron = library.patrons[patron_id]
        if not patron:
            raise ValueError(f"Patron with ID {patron_id} not found in the library_system")

        if library_item.isbn not in library.library_items:
            raise ValueError(f"Library item with ISBN {library_item.isbn} not found in the library_system")

        if library_item.is_borrowed:
            raise ValueError(f"Library item with ISBN {library_item.isbn} is already borrowed")

        patron.add_library_item_to_patron(library_item=library_item)
        library_item.is_borrowed = True
        export_data(library.library_items, '../data/library_items.csv', ["ISBN", "Type", "Title", "Is Borrowed?"],
                    item_row_preparer)
        logging.info(f"Library item {library_item.title} has been borrowed by patron {patron_id}")
    except ValueError as e:
        logging.error(f"Failed to borrow library_system item: {e}")
