# conftest.py

import pytest
from library_system.library import Library
from library_system.patrons.patron import Patron
from library_system.library_items.items import LibraryItem


@pytest.fixture
def library():
    return Library(name="Test Library")


@pytest.fixture
def sample_books():
    return [
        LibraryItem(isbn="123456789", title="Book 1", is_borrowed=False),
        LibraryItem(isbn="678901234", title="Book 2", is_borrowed=False)
    ]


def sample_library_item():
    return LibraryItem(isbn="123456784", title="Barca", is_borrowed=False)


@pytest.fixture
def sample_patrons():
    return [
        Patron(patron_id="123456789", name="PatronA"),
        Patron(patron_id="212345678", name="PatronB")
    ]
