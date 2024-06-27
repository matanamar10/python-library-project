import pytest
from library_system.library_items.items import LibraryItem
from library_system.management.borrowing_department import return_a_library_item, borrow_a_library_item
from unittest.mock import patch


def test_borrow_a_library_item(library, sample_library_item, patron):
    library.patrons[patron.patron_id] = patron
    library.library_items[sample_library_item.isbn] = sample_library_item

    borrow_a_library_item(library, sample_library_item, patron.patron_id)

    assert sample_library_item.is_borrowed
    assert sample_library_item in patron.borrowed_items


def test_borrow_a_library_item_nonexistent_patron(library, library_item):
    library.library_items[library_item.isbn] = library_item

    with pytest.raises(ValueError, match="Patron with ID .* not found"):
        borrow_a_library_item(library, library_item, "123456781")


def test_borrow_a_library_item_nonexistent_item(library, patron):
    library.patrons[patron.patron_id] = patron

    with pytest.raises(ValueError, match="Library item with ISBN .* not found"):
        borrow_a_library_item(library, LibraryItem(isbn="nonexistent_isbn", title="Nonexistent Book", item_type="book"),
                              patron.patron_id)


def test_borrow_a_library_item_already_borrowed(library, library_item, patron):
    library.patrons[patron.patron_id] = patron
    library.library_items[library_item.isbn] = library_item
    library_item.is_borrowed = True

    with pytest.raises(ValueError, match="Library item with ISBN .* is already borrowed"):
        borrow_a_library_item(library, library_item, patron.patron_id)


def test_return_a_library_item(library, library_item, patron):
    library.patrons[patron.patron_id] = patron
    library.library_items[library_item.isbn] = library_item
    library_item.is_borrowed = True
    patron.add_library_item_to_patron(library_item)

    with patch('library_system.management.finance.calculate_bill', return_value=0):
        return_a_library_item(library, library_item, patron.patron_id)

    assert not library_item.is_borrowed
    assert library_item not in patron.borrowed_items


def test_return_a_library_item_nonexistent_patron(library, library_item):
    library.library_items[library_item.isbn] = library_item
    library_item.is_borrowed = True

    with pytest.raises(ValueError, match="Patron with patron id .* was not found"):
        return_a_library_item(library, library_item, "nonexistent_patron")


def test_return_a_library_item_nonexistent_item(library, patron):
    library.patrons[patron.patron_id] = patron

    with pytest.raises(ValueError, match="The library_system item with isbn .* was not found"):
        return_a_library_item(library, LibraryItem(isbn="nonexistent_isbn", title="Nonexistent Book", item_type="book"),
                              patron.patron_id)


def test_return_a_library_item_not_borrowed(library, library_item, patron):
    library.patrons[patron.patron_id] = patron
    library.library_items[library_item.isbn] = library_item

    with pytest.raises(ValueError, match="Library item with ISBN .* is not borrowed"):
        return_a_library_item(library, library_item, patron.patron_id)


def test_return_a_library_item_with_outstanding_bills(library, library_item, patron):
    library.patrons[patron.patron_id] = patron
    library.library_items[library_item.isbn] = library_item
    library_item.is_borrowed = True
    patron.add_library_item_to_patron(library_item)

    with patch('library_system.management.finance.calculate_bill', return_value=10):
        with pytest.raises(ValueError, match="Patron .* needs to pay their bill before returning library_items"):
            return_a_library_item(library, library_item, patron.patron_id)
