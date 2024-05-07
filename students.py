# students.py is a file which represents the students - type of actually patron.
from patron import Patron
from datetime import datetime, timedelta
from book import Book


# The Student class inherit from Patron class , and manage all the students in the library.
class Student(Patron):
    def __init__(self, name, student_id, age):
        super().__init__(name, student_id)
        self.age = age
        self.books = {}

    # This function will add books to the student list - used when borrow a book action is performed
    def add_book_to_student(self, book=None):
        # Error Handling - validate that the customer provide a book instance.
        try:
            if isinstance(book, Book):
                # Error Handling - check if the book is for sure a borrowed one.
                if not book.is_borrowed:
                    self.books[book.isbn] = book
                    self.books[book.isbn].is_borrowed = True
                    self.books[book.isbn].borrowed_date = datetime.now()
                    self.books[book.isbn].due_date = self.books[book.isbn].borrowed_date + timedelta(days=14)
                    self.books[book.isbn].owner_id = self.patron_id
                else:
                    raise TypeError(f"Book is already Borrowed")
            else:
                raise TypeError(f"The object you have provided is not a Book type!")
        except TypeError as e:
            print(f"assign book to student has failed due to unexpected errors: {e}")

    # Used when user want to return a book to the library - delete the book from the user list.
    def remove_book_from_student(self, book=None):
        # Error handling - make sure that book is borrowed
        try:
            if book.is_borrowed:
                # Remove the book from the student
                del self.books[book.isbn]
                book.is_borrowed = False
            else:
                raise ValueError(f"Book is already not borrowed...")
        except ValueError as e:
            print(f"Tried to remove the book from this student - action failed due to error: {e}")

    # Function to calculate the student bills.
    def calculate_bill(self):
        calculated_bill = 0
        check_date = datetime.now()
        for book_isbn, book in self.books.items():
            if check_date > book.due_date:
                days_late = (check_date - book.due_date).days
                fine = days_late * 0.50  # Example fine calculation: $0.50 per day late
                calculated_bill = calculated_bill + fine
            else:
                print(f"There isn't any bill to add for this book!")
        return calculated_bill
