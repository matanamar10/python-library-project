# book.py
import logging

from utils import contain_non_letters


class Book:
    def __init__(self, title, author, isbn):
        self.is_borrowed = False
        self.title = title
        self.author = author
        self.isbn = isbn
        self.borrowed_date = None
        self.due_date = None
        self.owner_id = None

    def verify_book_details(self):
        try:
            # Check if ISBN has exactly 9 digits
            if len(self.isbn) != 9:
                raise ValueError(f"ISBN must be exactly nine digits long, but it has {len(self.isbn)} digits.")

            # Check if author name contains only letters
            if contain_non_letters(self.author):
                raise ValueError("The author name should contain only letters.")

            # If no errors were raised, return True
            logging.info("The book details are verified successfully")
            return True

        except ValueError as e:
            # Handle ValueError exceptions
            print(f"Verification failed: {e}")
            return False
