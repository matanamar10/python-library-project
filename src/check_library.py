from controllers.library import Library
from models.entities.library_items import Book
from models.entities.patrons.students.students import Student
from models.entities.patrons import Teacher
from controllers.management.borrowing_department import BorrowingDepartment


def check_library():
    borrowing_department = BorrowingDepartment()
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

    borrowing_department.borrow_library_item(my_library, book1, student3.patron_id)
    my_library.add_new_patron_to_the_library(teachers)

    borrowing_department.return_a_library_item(my_library, book1, student3.patron_id)
    borrowing_department.borrow_library_item(my_library, book1, student3.patron_id)

    my_library.add_new_library_items_to_the_library(books)
