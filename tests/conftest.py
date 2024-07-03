import mongomock
import pytest
from library_system.library import Library


@pytest.fixture(scope='module')
def mock_db():
    client = mongomock.MongoClient()
    db = client.library
    db['library-items'].insert_one({'isbn': '123456789', 'title': 'Test Book', 'is_borrowed': False})
    db['library-patrons'].insert_one({'patron_id': '111111111', 'name': 'Test Patron', 'patron_items': {}})
    return db


@pytest.fixture
def library():
    return Library(name="TestLibrary")


@pytest.fixture


@pytest.fixture
