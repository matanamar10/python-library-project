import mongomock
import pytest
from controllers.library import Library
from models.patrons.students import Student
from models.library_items.books.book import Book


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
def library_item():
    return Book(isbn='123456789', title="Example", author="SnoopDog")


@pytest.fixture
def not_exist_library_item():
    return Book(isbn='123456444', title="WinterInTheWindow", author="PeerTasi")


@pytest.fixture
def patron():
    patron = Student(patron_id='123456123', name="Greg", age=20)
    return patron


@pytest.fixture
def not_exist_patron():
    patron = Student(patron_id='123456781', name="Josh", age=30)
    return patron


@pytest.fixture(autouse=True)
def library_items():
    library_item_1 = Book(isbn='123456789', title="Example", author="SnoopDog")
    library_item_2 = Book(isbn='123456788', title="Exam", author="SnoopDob")
    library_item_3 = Book(isbn='123321456', title="SDS", author="Panda")
    new_library_items = [library_item_1, library_item_2, library_item_3]
    return new_library_items


@pytest.fixture
def library_item_borrowed():
    return Book(isbn="123765912", title="TestBorrowedBook", is_borrowed=True, author="EyalGolan")


@pytest.fixture
def new_library_item():
    return Book(isbn="678901342", title="NewBook", is_borrowed=False, author="DuduGoresh")


@pytest.fixture
def new_patron():
    return Student(patron_id="102345679", name="Jane Smith", age=44)
