import logging
from exporter.export_data_to_excel import export_library_attributes
from library_objects.finance import calculate_bill
from library_objects.library import Library
from library_objects.items import LibraryItem


def return_a_library_item(library: Library, library_item: LibraryItem, patron_id: str):
    """
    The function return_a_library_item is help to the library to manage the library items that customers want to return
    after they borrowed them.

    The function get as parameters :
    1. Library - The Library object itself
    2. Library_item - book/disk to return
    3. patron_id - the string which represent the patron id - the customer id.
    """

    try:
        patron = library.patrons[patron_id]
        if not patron:
            raise ValueError(f"Patron with patron id {patron_id} was not found in the library")
        if library_item.isbn not in library.library_items.keys():
            raise ValueError(f"The library item with isbn {library_item.isbn} was not found in the library")
        if not library_item.is_borrowed:
            raise ValueError(f"Library item with ISBN {library_item.isbn} is not borrowed")
        patron_calculated_bill = calculate_bill(patron=patron)
        library.bills[patron_id] = patron_calculated_bill
        if library.bills[patron_id] != 0:
            raise ValueError(f"Patron {patron_id} needs to pay their bill before returning items")
        patron.remove_library_item_from_patron(library_item)
        library_item.is_borrowed = False  # The book is not borrowed anymore.
        export_library_attributes(library.library_items, attribute_type="items")
        logging.info(f"Library item {library_item.title} has been returned by patron {patron_id}")
    except ValueError as e:
        logging.error(f"Failed to return library item: {e}")


def borrow_a_library_item(library: Library, library_item: LibraryItem, patron_id: str):
    """
    The function borrow_a_library_item is help to the library to manage the library items that customers want to borrow
    after they borrowed them.

    The function get as parameters :
    1. Library - The Library object itself
    2. Library_item - book/disk to borrow
    3. patron_id - the string which represent the patron id - the customer id
    """

    try:
        patron = library.patrons[patron_id]
        if not patron:
            raise ValueError(f"Patron with ID {patron_id} not found in the library")

        if library_item.isbn not in library.library_items:
            raise ValueError(f"Library item with ISBN {library_item.isbn} not found in the library")

        if library_item.is_borrowed:
            raise ValueError(f"Library item with ISBN {library_item.isbn} is already borrowed")

        patron.add_library_item_to_patron(library_item=library_item)
        library_item.is_borrowed = True
        export_library_attributes(library.library_items, attribute_type="items")
        logging.info(f"Library item {library_item.title} has been borrowed by patron {patron_id}")
    except ValueError as e:
        logging.error(f"Failed to borrow library item: {e}")
