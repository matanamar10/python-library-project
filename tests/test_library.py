import pytest
from library_system.library import Library
from library_system.library_items.items import LibraryItem
from library_system.patrons.patron import Patron


@pytest.fixture
def library():
    return Library(name="Test Library")


@pytest.fixture
def sample_books():
    return [
        LibraryItem(isbn="123456789", title="Book 1", is_borrowed=False),
        LibraryItem(isbn="678901234", title="Book 2", is_borrowed=False)
    ]


@pytest.fixture
def sample_patrons():
    return [
        Patron(patron_id="123456789", name="PatronA"),
        Patron(patron_id="212345678", name="PatronB")
    ]


def test_add_new_library_items_to_the_library(library, sample_books):
    library.add_new_library_items_to_the_library(sample_books)
    assert "123456789" in library.library_items
    assert "212345678" in library.library_items


def test_add_new_library_items_to_the_library_duplicate(library, sample_books):
    library.add_new_library_items_to_the_library(sample_books)
    with pytest.raises(ValueError):
        library.add_new_library_items_to_the_library(sample_books)


def test_add_new_patron_to_the_library(library, sample_patrons):
    library.add_new_patron_to_the_library(sample_patrons)
    assert "123456789" in library.patrons
    assert "212345678" in library.patrons


def test_add_new_patron_to_the_library_duplicate(library, sample_patrons):
    library.add_new_patron_to_the_library(sample_patrons)
    with pytest.raises(ValueError):
        library.add_new_patron_to_the_library(sample_patrons)


def test_remove_patrons_from_the_library(library, sample_patrons):
    library.add_new_patron_to_the_library(sample_patrons)
    library.remove_patrons_from_the_library([sample_patrons[0]])
    assert "123456789" not in library.patrons
    assert "212345678" in library.patrons


def test_remove_patrons_from_the_library_not_exist(library, sample_patrons):
    with pytest.raises(ValueError):
        library.remove_patrons_from_the_library([sample_patrons[0]])


def test_search_library_items(library, sample_books):
    library.add_new_library_items_to_the_library(sample_books)
    results = library.search_library_items(library_item_title="Book 1")
    assert "Book 1" in results


def test_remove_library_item_from_the_library(library, sample_books):
    library.add_new_library_items_to_the_library(sample_books)
    library.remove_libray_item_from_the_library("12345")
    assert "123456788" not in library.library_items


def test_remove_library_item_from_the_library_not_exist(library):
    with pytest.raises(ValueError):
        library.remove_libray_item_from_the_library("999999999")


def test_remove_library_item_from_the_library_borrowed(library, sample_books):
    library.add_new_library_items_to_the_library(sample_books)
    library.library_items["123456789"].is_borrowed = True
    with pytest.raises(ValueError):
        library.remove_libray_item_from_the_library("12345")
