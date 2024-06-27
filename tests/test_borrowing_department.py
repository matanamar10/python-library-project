import pytest
from library_system.library_items.items import LibraryItem


    library.patrons[patron.patron_id] = patron




    library.library_items[library_item.isbn] = library_item



    library.patrons[patron.patron_id] = patron



def test_borrow_a_library_item_already_borrowed(library, library_item, patron):
    library.patrons[patron.patron_id] = patron
    library.library_items[library_item.isbn] = library_item
    library_item.is_borrowed = True

        borrow_a_library_item(library, library_item, patron.patron_id)


    library.patrons[patron.patron_id] = patron
    library.library_items[library_item.isbn] = library_item
    library_item.is_borrowed = True
    patron.add_library_item_to_patron(library_item)

    return_a_library_item(library, library_item, patron.patron_id)



    library.library_items[library_item.isbn] = library_item
    library_item.is_borrowed = True



    library.patrons[patron.patron_id] = patron


def test_return_a_library_item_not_borrowed(library, library_item, patron):
    library.patrons[patron.patron_id] = patron
    library.library_items[library_item.isbn] = library_item

        return_a_library_item(library, library_item, patron.patron_id)


def test_return_a_library_item_with_outstanding_bills(library, library_item, patron):
    library.patrons[patron.patron_id] = patron
    library.library_items[library_item.isbn] = library_item
    library_item.is_borrowed = True
    patron.add_library_item_to_patron(library_item)

    with patch('library_system.management.finance.calculate_bill', return_value=10):
            return_a_library_item(library, library_item, patron.patron_id)
