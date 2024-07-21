import logging

from controllers.library import Library
from models.library_items.books.book import Book
from models.patrons.students import Student
from models.patrons.teacher import Teacher
from controllers.management.borrowing_department import borrow_a_library_item, return_a_library_item
from mongodb.mongo_setup import connect_to_mongodb, disconnect_from_mongodb
from utils.custom_errors import *


def main():
    try:
        connect_to_mongodb()
        my_library = Library(name="Amar-Library")
        student2 = Student(patron_id='123456777', name="Oran", age=21)
        student3 = Student(patron_id='123456123', name="Greg", age=20)
        students = [student3, student2]
        book1 = Book(isbn='123456789', title="Example", author="SnoopDog")
        book2 = Book(isbn='123456788', title="Exam", author="SnoopDob")
        books = [book1, book2]
        teacher1 = Teacher(name="One", patron_id="123123123")
        teacher2 = Teacher(name="Two", patron_id="123123144")
        teachers = [teacher1, teacher2]
        my_library.add_new_library_items_to_the_library(books)
        my_library.add_new_patron_to_the_library(students)
        borrow_a_library_item(my_library, book1, student3.patron_id)
        my_library.add_new_patron_to_the_library(teachers)
        return_a_library_item(my_library, book1, student3.patron_id)
        borrow_a_library_item(my_library, book1, student3.patron_id)
        my_library.add_new_library_items_to_the_library(books)
    except NotUniqueLibraryItemError as e:
        logging.error(f"Library item already exists: {e}")
        raise
    except NotUniquePatronError as e:
        logging.error(f"Patron already exists: {e}")
        raise
    except OutstandingBillError as e:
        logging.error(f"Outstanding bill: {e}")
        raise
    except NotExistingPatron as e:
        logging.error(f"Patron not found: {e}")
        raise
    except NotExistingLibraryItem as e:
        logging.error(f"Library item not found: {e}")
        raise
    except ExistingBillToPay as e:
        logging.error(f"Outstanding bill: {e}")
        raise
    except NotBorrowedLibraryItem as e:
        logging.error(f"Item not borrowed: {e}")
        raise
    except BorrowedLibraryItem as e:
        logging.error(f"Item already borrowed: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise
    finally:
        disconnect_from_mongodb()


if __name__ == "__main__":
    main()
