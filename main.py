# main.py

from library import Library
from book import Book
from students import Student
from teacher import Teacher

my_library = Library(name="AmarLibrary")
student1 = Student(student_id='123456789', name="Matan", age=21)
student2 = Student(student_id='123456777', name="Oran", age=21)
student3 = Student(student_id='123456123', name="Greg", age=20)
students = [student3, student2]
book1 = Book(isbn='123456789', title="Example", author="SnoopDog")
book2 = Book(isbn='123456788', title="Exam", author="SnoopDob")
book3 = Book(isbn='123321456', title="SDS", author="Panda")
books = [book1, book2]
teacher1 = Teacher(name="One", teacher_id="123123123")
teacher2 = Teacher(name="Two", teacher_id="123123144")
teacher3 = Teacher(name="Three", teacher_id="312321232")
teachers = [teacher1, teacher2]
my_library.add_new_books_to_the_library(books)
my_library.add_new_patron_to_the_library(patron_type='Student', patrons=students)
my_library.add_new_patron_to_the_library(patron_type='Student', patrons=student3)
my_library.borrow_a_book(book=book1, student_id=student3.patron_id)
my_library.add_new_patron_to_the_library(patron_type='Teacher', patrons=teachers)
my_library.add_students_to_a_teacher(teacher_id='123123144', students=students)


