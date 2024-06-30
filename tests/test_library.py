import pytest


def test_add_new_library_items_to_the_library(library, new_library_item):
    library.add_new_library_items_to_the_library([new_library_item])
    assert new_library_item.isbn in library.library_items.keys()
    assert library.library_items[new_library_item.isbn] == new_library_item


def test_add_existing_library_items_to_the_library(library, library_item):
    library.add_new_library_items_to_the_library([library_item])
    with pytest.raises(ValueError):
        library.add_new_library_items_to_the_library([library_item])


def test_add_new_patron_to_the_library(library, new_patron):
    library.add_new_patron_to_the_library([new_patron])
    assert new_patron.patron_id in library.patrons
    assert library.patrons[new_patron.patron_id] == new_patron


def test_add_existing_patron_to_the_library(library, patron):
    library.add_new_patron_to_the_library([patron])
    with pytest.raises(ValueError):
        library.add_new_patron_to_the_library([patron])


def test_remove_patrons_from_the_library(library, patron):
    library.add_new_patron_to_the_library([patron])
    library.remove_patrons_from_the_library([patron])
    assert patron.patron_id not in library.patrons


def test_remove_nonexistent_patron_from_the_library(library, patron):
    with pytest.raises(ValueError):
        library.remove_patrons_from_the_library([patron])


def test_search_library_items_by_title(library, library_item):
    library.add_new_library_items_to_the_library([library_item])
    results = library.search_library_items(library_item_title=library_item.title)
    assert library_item.title in results


def test_search_library_items_by_isbn(library, library_item):
    library.add_new_library_items_to_the_library([library_item])
    results = library.search_library_items(library_item_isbn=library_item.isbn)
    assert library_item.isbn in results


def test_remove_library_item_from_the_library(library, library_item):
    library.add_new_library_items_to_the_library([library_item])
    library.remove_libray_item_from_the_library(library_item.isbn)
    assert library_item.isbn not in library.library_items


def test_remove_nonexistent_library_item_from_the_library(library):
    with pytest.raises(ValueError):
        library.remove_libray_item_from_the_library("nonexistent_isbn")


def test_remove_borrowed_library_item_from_the_library(library, library_item_borrowed):
    library.add_new_library_items_to_the_library([library_item_borrowed])
    with pytest.raises(ValueError):
        library.remove_libray_item_from_the_library(library_item_borrowed.isbn)
