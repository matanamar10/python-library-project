# main.py

from library_system.library import Library
from library_system.library_items.books.book import Book
from library_system.patrons.students import Student
from library_system.patrons.teacher import Teacher
from library_system.management.borrowing_department import borrow_a_library_item, return_a_library_item

my_library = Library(name="Amar-Library")
student1 = Student(patron_id='123456789', name="Matan", age=21)
student2 = Student(patron_id='123456777', name="Oran", age=21)
student3 = Student(patron_id='123456123', name="Greg", age=20)
students = [student3, student2]
book1 = Book(isbn='123456789', title="Example", author="SnoopDog")
book2 = Book(isbn='123456788', title="Exam", author="SnoopDob")
book3 = Book(isbn='123321456', title="SDS", author="Panda")
books = [book1, book2]
teacher1 = Teacher(name="One", patron_id="123123123")
teacher2 = Teacher(name="Two", patron_id="123123144")
teacher3 = Teacher(name="Three", patron_id="312321232")
teachers = [teacher1, teacher2]
my_library.add_new_library_items_to_the_library(books)
my_library.add_new_patron_to_the_library(students)
borrow_a_library_item(my_library, book1, student3.patron_id)
my_library.add_new_patron_to_the_library(teachers)
return_a_library_item(my_library, book1, student3.patron_id)
borrow_a_library_item(my_library, book1, student3.patron_id)
