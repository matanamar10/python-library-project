# python-library-project
# Project of Library management in python 

# Introduction
This Library Management System is designed to manage books, patrons (students and teachers), and borrowing activities within a library. It offers a complete suite of functionalities including adding and removing books and patrons, borrowing and returning books, and exporting library data to CSV files. This system aims to streamline the library operations and improve the management of library resources.

## System Architecture

The Library Management System is designed to facilitate the management of a library's resources including books, patrons (students and teachers), and borrowing activities. It is structured around several key 
classes, each responsible for handling specific aspects of the library operations.

# Class Descriptions
For each class, provide a brief description, list its main responsibilities, and describe its relationships with other classes. Include details about key methods and attributes.

1. Book Class
### Book Class

**Responsibilities:**
- Store details about a book such as title, author, ISBN, and its borrowing status.

**Attributes:**
- `title`: The title of the book.
- `author`: The author of the book.
- `isbn`: The ISBN number of the book, acts as a unique identifier.
- `is_borrowed`: A boolean that indicates whether the book is currently borrowed.
- `borrowed_date`: The date when the book was borrowed.
- `due_date`: The date when the book is due for return.

**Methods:**
- `verify_book_details()`: Ensures all book details meet the required standards for entry into the system.
2. Patron Class (and its subclasses Student and Teacher)
### Patron Class

**Responsibilities:**
- Abstract base class for patrons of the library, defining common attributes and methods for derived classes (Student, Teacher).

**Attributes:**
- `name`: The name of the patron.
- `patron_id`: A unique identifier for the patron.

**Subclasses:**
- `Student`
- `Teacher`

### Student Class

**Responsibilities:**
- Manage information and operations specific to students, such as borrowing books.

**Attributes:**
- Inherits all attributes from `Patron`.
- `books`: A dictionary of books currently borrowed by the student.

### Teacher Class

**Responsibilities:**
- Manage information specific to teachers, possibly including a list of students advised.

**Attributes:**
- Inherits all attributes from `Patron`.
- `students`: A dictionary of students under the teacher’s advisement.
3. Library Class
### Library Class

**Responsibilities:**
- Main class managing the overall library operations.
- Handles adding/removing books and patrons, checking in and checking out books.

**Attributes:**
- `books`: A dictionary storing all books within the library, keyed by ISBN.
- `students`: A dictionary of all students, keyed by student ID.
- `teachers`: A dictionary of all teachers, keyed by teacher ID.
- `bills`: A dictionary tracking any outstanding fees for each student.

**Methods:**
- `add_new_books_to_the_library()`: Add new books to the collection.
- `add_new_patron_to_the_library()`: Register new patrons.
- `export_to_csv()`: Export all data into CSV format for reporting and backup.


# Features
# Manage Books:  
Add, remove, and search for books using ISBN, title, or author.
# Manage Patrons: 
* Add or remove students and teachers, and manage their details.
* Borrow and Return Books: Handle the borrowing and returning processes of books, including due date management and overdue fine calculations.
* Data Export: Export books, students, teachers, and billing information to CSV files for record-keeping.
* Bill Management: Calculate and update bills for borrowed books, especially when they are overdue.

# Architecture Conclusion:
These classes and their methods interact to facilitate the efficient management of library resources, ensuring that users can borrow and return books seamlessly, and that library administrators can maintain accurate and up-to-date records.


  
# Installation
# Clone the Repository:
* Copy code:
  git clone https://github.com/matanamar10/python-library-project.git
  cd python-library-project
# Install Dependencies:
Ensure that Python 3.10 is installed on your system. You can download it from python.org.
Setup Environment:
It's recommended to create a virtual environment for Python projects.
# Starting the Library System
You can start interacting with the library system by creating an instance of the Library class:
# Create a library instance
lib = Library("Central Library")
Adding a Book
To add a book to the library:

from book import Book

new_book = Book("1984", "George Orwell", "123456789")
lib.add_new_books_to_the_library(new_book)
Adding a Patron
To add a student or teacher to the library:

from patron import Student, Teacher  

new_student = Student("John Doe", "000000001", 20)
lib.add_new_patron_to_the_library('Student', new_student)

new_teacher = Teacher("Jane Doe", "000000002")
lib.add_new_patron_to_the_library('Teacher', new_teacher)
# Borrowing a Book
To borrow a book:

lib.borrow_a_book(new_book, new_student.patron_id)
Returning a Book
To return a book:
lib.return_a_book(new_book, new_student.patron_id)


# Contributing
Contributions to this project are welcome! Here's how you can contribute:

Fork the Repository: Fork the project to your own GitHub account.
Create a Feature Branch: Create a branch in your forked repository for your contribution.
Commit Your Changes: Make your changes and commit them with a clear commit message.
Push to the Branch: Push your changes to your repository.
Submit a Pull Request: Open a pull request from your feature branch to the original repository.
