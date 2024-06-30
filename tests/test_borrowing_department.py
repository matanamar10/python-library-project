import pytest
from unittest.mock import patch
from library_system.library_items.items import LibraryItem
from library_system.management.borrowing_department import borrow_a_library_item, return_a_library_item


def test_borrow_a_library_item_success(library, library_item, patron):
    library.patrons[patron.patron_id] = patron
    library.library_items[library_item.isbn] = library_item

    borrow_a_library_item(library, library_item, patron.patron_id)

    assert library_item.is_borrowed, "The library item should be marked as borrowed"
    assert library_item.isbn in patron.patron_items.keys(), ("The library item should be in the patron's borrowed "
                                                             "items list")


def test_borrow_a_library_item_patron_not_exist(library, library_item, not_exist_patron):
    library.library_items[library_item.isbn] = library_item

    with pytest.raises(ValueError,
                       match=f"Patron with ID {not_exist_patron.patron_id} not found in the library_system"):
        borrow_a_library_item(library, library_item, not_exist_patron.patron_id)


def test_borrow_a_library_item_item_not_exist(library, not_exist_library_item, patron):
    library.patrons[patron.patron_id] = patron

    with pytest.raises(ValueError,
                       match=f"Library item with ISBN {not_exist_library_item.isbn} not found in the library_system"):
        borrow_a_library_item(library, not_exist_library_item, patron.patron_id)


def test_borrow_a_library_item_already_borrowed(library, library_item, patron):
    library.patrons[patron.patron_id] = patron
    library.library_items[library_item.isbn] = library_item
    library_item.is_borrowed = True

    with pytest.raises(ValueError, match=f"Library item with ISBN {library_item.isbn} is already borrowed"):
        borrow_a_library_item(library, library_item, patron.patron_id)


def test_return_a_library_item_success(library, library_item, patron):
    library.patrons[patron.patron_id] = patron
    library.library_items[library_item.isbn] = library_item
    library_item.is_borrowed = True
    patron.add_library_item_to_patron(library_item)

    return_a_library_item(library, library_item, patron.patron_id)

    assert not library_item.is_borrowed, "The library item should no longer be marked as borrowed"
    assert library_item.isbn not in patron.patron_items.keys(), (
        "The library item should be removed from the patron's borrowed "
        "items list")


def test_return_a_library_item_patron_not_exist(library, library_item, not_exist_patron):
    library.library_items[library_item.isbn] = library_item
    library_item.is_borrowed = True

    with pytest.raises(ValueError,
                       match=f"Patron with patron id {not_exist_patron.patron_id} was not found in the library_system"):
        return_a_library_item(library, library_item, not_exist_patron)


def test_return_a_library_item_item_not_exist(library, not_exist_library_item, patron):
    library.patrons[patron.patron_id] = patron
    with pytest.raises(ValueError,
                       match=f"The library_system item with isbn {not_exist_library_item.isbn} was not found in the "
                             f"library_system"):
        return_a_library_item(library, not_exist_library_item, patron.patron_id)


def test_return_a_library_item_not_borrowed(library, library_item, patron):
    library.patrons[patron.patron_id] = patron
    library.library_items[library_item.isbn] = library_item

    with pytest.raises(ValueError, match=f"Library item with ISBN {library_item.isbn} is not borrowed"):
        return_a_library_item(library, library_item, patron.patron_id)


def test_return_a_library_item_with_outstanding_bills(library, library_item, patron):
    library.patrons[patron.patron_id] = patron
    library.library_items[library_item.isbn] = library_item
    library_item.is_borrowed = True
    patron.add_library_item_to_patron(library_item)

    with patch('library_system.management.finance.calculate_bill', return_value=10):
        with pytest.raises(ValueError,
                           match=f"Patron {patron.name} needs to pay their bill before returning library_items"):
            return_a_library_item(library, library_item, patron.patron_id)
