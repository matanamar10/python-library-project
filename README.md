# python-library-project
# Project of Library management in python 

# Introduction
This Library Management System is designed to manage books, patrons (students and teachers), and borrowing activities within a library. It offers a complete suite of functionalities including adding and removing books and patrons, borrowing and returning books, and exporting library data to CSV files. This system aims to streamline the library operations and improve the management of library resources.

# Features
# Manage Books:  
Add, remove, and search for books using ISBN, title, or author.
# Manage Patrons: 
* Add or remove students and teachers, and manage their details.
* Borrow and Return Books: Handle the borrowing and returning processes of books, including due date management and overdue fine calculations.
* Data Export: Export books, students, teachers, and billing information to CSV files for record-keeping.
* Bill Management: Calculate and update bills for borrowed books, especially when they are overdue.
  
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
