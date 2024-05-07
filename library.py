# library.py
from utils import convert_to_list
from utils import is_library_element_exists
from datetime import datetime, timedelta
import csv


class Library:
    def __init__(self, name):
        self.books = {}  # Dict to represent books and their state
        self.teachers = {}
        self.students = {}
        self.name = name
        self.last_exported_data = None  # Store the last exported data
        self.bills = {}

    # Function to export all the library data to xlsx file
    def export_to_csv(self):
        try:
            # Write data for Books
            with open("books.csv", mode="w", newline='') as books_file:
                books_writer = csv.writer(books_file)
                books_writer.writerow(["ISBN", "Title", "Author", "Is Borrowed?", "Due Date", "Owner_ID"])
                for book_isbn, book in self.books.items():
                    books_writer.writerow(
                        [book_isbn, book.title, book.author, book.is_borrowed, book.due_date, book.owner_id])

            # Write data for Students
            with open("students.csv", mode="w", newline='') as students_file:
                students_writer = csv.writer(students_file)
                students_writer.writerow(["ID", "Name", "Books"])
                for student_id, student in self.students.items():
                    students_writer.writerow([student_id, student.name, student.books.keys()])

            # Write data for Teachers
            with open("teachers.csv", mode="w", newline='') as teachers_file:
                teachers_writer = csv.writer(teachers_file)
                teachers_writer.writerow(["ID", "Name", "Students"])
                for teacher_id, teacher in self.teachers.items():
                    teachers_writer.writerow([teacher_id, teacher.name, teacher.students.keys()])

            # Write data for Bills
            with open("bills.csv", mode="w", newline='') as bills_file:
                bills_writer = csv.writer(bills_file)
                bills_writer.writerow(["Student ID", "Calculated Bill"])
                for student_id, bill in self.bills.items():
                    bills_writer.writerow([student_id, bill])

            print("Data exported to CSV files successfully!")
        except Exception as e:
            print(f"An error occurred while exporting to CSV: {e}")

    def update_excel_file(self):
        self.export_to_csv()

    def get_library_details(self):
        print(f"You are in: \n {self.name} library")

    # This functions allow us to add one or more new none-exists books to the library system
    def add_new_books_to_the_library(self, new_books):
        new_books_to_add = convert_to_list(new_books)
        try:
            for new_book in new_books_to_add:
                # The verify_book_details method verify the spelling and writing convention of books in the library
                # For example: The isbn of book must contain exact 9 digits
                if new_book.verify_book_details():
                    if new_book.isbn not in self.books.keys():
                        self.books[new_book.isbn] = new_book
                        print(f"The book {new_book.title} with isbn {new_book.isbn} is added to '{self.name}' library")
                        # At the end of each method which manipulate the library system , we need to perform update to
                        # the Excel file .
                        self.update_excel_file()
                    else:
                        raise ValueError(
                            f"The book {new_book.title} with isbn {new_book.isbn} is already exists in system!")
                else:
                    raise ValueError(f"The book verification has been failed.")

        except ValueError as e:
            print(f"Add book failed: {e}")

    # This function adds new students or teachers by provided type - to the library system.
    def add_new_patron_to_the_library(self, patron_type, patrons):
        # The convert_to_list method is giving the user the option to mention either one or more new books to add.
        patrons = convert_to_list(patrons)
        try:
            for patron in patrons:
                if patron.verify_patron_details():
                    # The verify_book_details method verify the spelling and writing convention of books in the library
                    # For example: The isbn of book must contain exact 9 digits
                    if patron_type == 'Student':
                        # The is_library_element_exists method checks if the patron already exists in the library system
                        if patron.patron_id not in self.students:
                            # The add_to_dict method is adding each patron to his relevant dict
                            self.students[patron.patron_id] = patron
                            print(f"The student {patron.patron_id} is added successfully to the library")
                            self.update_excel_file()
                        else:
                            raise ValueError(f"The student with id {patron.patron_id} already exists in the library")
                    elif patron_type == 'Teacher':
                        # The is_library_element_exists method checks if the patron already exists in the library system
                        if patron.patron_id not in self.teachers:
                            # The add_to_dict method is adding each patron to his relevant dict
                            self.teachers[patron.patron_id] = patron
                            print(f"The teacher {patron.patron_id} is added successfully to the library")
                            self.update_excel_file()
                        else:
                            raise ValueError(f"The teacher with id {patron.patron_id} already exists in the library")
                    else:
                        raise TypeError(
                            f"The type provided need to be string with the values 'Student' or 'Teacher only!")
                else:
                    raise ValueError(
                        f"The verification of the patrons details you gave are failed - check them all again!")
        except ValueError as v:
            print(f"Patron addition action failed due to error: {v}")
        except TypeError as t:
            print(f"Patron addition action failed due to errors: {t}")

    # This function will remove existing patrons , students or teachers - from the library
    def remove_patrons_from_the_library(self, patron_type, patrons):
        patrons = convert_to_list(patrons)
        try:
            for patron in patrons:
                if patron.verify_patron_details():
                    if patron_type == 'Student':
                        if is_library_element_exists(self.students, patron.patron_id):
                            del self.students[patron.patron_id]
                            print(f"The student {patron.patron_id} is removed successfully from the library")
                            self.update_excel_file()
                        else:
                            raise ValueError(f"The student isn't exists")
                    elif patron_type == 'Teacher':
                        if is_library_element_exists(self.teachers, patron.patron_id):
                            del self.teachers[patron.patron_id]
                            print(f"The teacher {patron.patron_id} is removed successfully from the library")
                            self.update_excel_file()
                        else:
                            raise ValueError(f"The teacher isn't exists")
                    else:
                        raise TypeError(
                            f"The patrons type you gave are wrong - patron could be just Teacher or Student")
                else:
                    raise ValueError(f"The verification has failed for this patron - fix it!")
        except ValueError as v:
            print(f"Patron addition action failed due to error: {v}")
        except TypeError as t:
            print(f"Patron addition action failed due to errors: {t}")

    # This function will make a book borrowed - it will add a book to a student , and manipulate the book fields.
    # For example: The is_borrowed field will become "True".
    def borrow_a_book(self, book, student_id):
        # Verifying the student and book details
        try:
            if book.isbn in self.books and student_id in self.students:
                # Verifying that the relevant book isn't borrowed already.
                if not book.is_borrowed:
                    student = (self.students[student_id])
                    # Assign the book to the student - adding the book to the student books dict.
                    student.add_book_to_student(book=book)
                    # Edit book fields to make him borrowed.
                    book.is_borrowed = True
                    book.borrowed_date = datetime.now()
                    book.due_date = book.borrowed_date + timedelta(days=14)
                    book.owner_id = student_id
                    self.update_excel_file()
                    print(f"book borrowed successfully")
                else:
                    raise ValueError(f"The book is already borrowed")
            else:
                raise ValueError(f"The Student {student_id} or the book {book.title} is not exist in our system")
        except ValueError as e:
            print(f"borrowing action failed due to errors: {e}")

    # This function is allow to users return a borrowed book.
    def return_a_book(self, book, student_id):
        # Verify the book&students details and check if for sure the book is borrowed at all.
        try:
            if book.isbn in self.books.keys() and book.is_borrowed and student_id in self.students:
                student = self.students[student_id]
                print(student.patron_id)
                # Check for student bills to pay - if exists - cannot return the item
                self.update_bills()
                if student_id not in self.bills or self.bills[student_id] == 0:
                    # Unassociated book from the student books dict and make him not borrowed
                    student.remove_book_from_student(book)
                    # Manipulate the book fields.
                    book.is_borrowed = False
                    book.borrowed_date = None
                    book.due_date = None
                    self.update_excel_file()
                    print(
                        f"The book {book.title} is returned to the library by student {student.name} - back to business!")
                else:
                    raise ValueError(
                        f"The book {book.title} cannot be returned because student {student.patron_id} got bills!")
            else:
                raise ValueError(f"The book is {book} isn't borrowed yet or it does not belongs to any student")
        except ValueError as v:
            print(f"The returning a book action failed due to error: {v}")

    # Function to filter on the library books and give the user to search book by isbn , authors or titles.
    def search_books(self, book_title=None, book_author=None, book_isbn=None):
        # The results list is a list where all the filter results will be saved
        results = []
        for book_isbn, book in self.books.items():
            # The filtering by the user-provided option (titles , authors or ISBNs)
            if (book_title is None or book.title in book_title) or \
                    (book_author is None or book.author in book_author) or \
                    (book_isbn is None or book.isbn == book_isbn):
                results.append(book.title)
        print(f"Those are the filter matches: \n ")
        for result in results:
            print(result)
        return results

    # Function that run every day & when customer come to return a book and check bills to pay on borrowed books.
    def update_bills(self):
        for student_id, student in self.students.items():
            # The calculate bill function used to calculate the exact bill of each student on each book
            bill = student.calculate_bill()
            if bill > 0:
                self.bills[student_id] = bill
                print(f"The student {student.name} has now a bill of {bill}")

    # Function to delete existing books from the library
    def remove_book_from_the_library(self, book_isbn):
        try:
            # Check if the book isbn which provided by user is it exist in the books dictionary
            if book_isbn in self.books.keys():
                book_title = self.books[book_isbn].title
                # Remove the book from the library system
                del self.books[book_isbn]
                print(f"The book {book_title} is removed from the library")
                self.update_excel_file()
                # Return True if succeed , False if it doesn't
            else:
                raise ValueError(f"the book with isbn {book_isbn} is already not in the library")
        except ValueError as e:
            print(f"The book deletion failed due to this error: {e}")

    # Assign students to specific teacher - Add students to the teachers students dictionary.
    def add_students_to_a_teacher(self, teacher_id, students):
        # Check if teacher_id is already exist
        try:
            if teacher_id in self.teachers.keys():
                teacher = self.teachers[teacher_id]
                students_list = convert_to_list(students)
                for student in students_list:
                    # Check if student is not already associate
                    if student not in teacher.students:
                        teacher.students[student.patron_id] = student
                        self.update_excel_file()
                        print(f"student {student.name} is now associate with {teacher.name}")
                    else:
                        raise ValueError(f"student {student.name} is already associate with teacher {teacher.name}")
            else:
                raise ValueError(f"teacher doesn't exists")
        except ValueError as e:
            print(f"The action of assign students to the teacher has failed due to error:{e}")

    def remove_students_from_teacher(self, teacher_id, students_id):
        teacher = self.teachers[teacher_id]
        # Check if teacher exists in the teachers directory
        try:
            if teacher in self.teachers.values():
                students_id_list = convert_to_list(students_id)
                for student_id in students_id_list:
                    # Check if student really assign to this teacher
                    if student_id in teacher.students.keys():
                        # Remove the student from the teacher list
                        del teacher.students[student_id]
                        self.update_excel_file()
                        print(f"student {student_id} removed successfully")
                    else:
                        raise ValueError(f"student {student_id} isn't associate with teacher {teacher.name}")
            else:
                raise ValueError(f"teacher {teacher_id} doesn't exists")
        except ValueError as e:
            print(f"The deletion of students from the teacher has failed due to those errors: {e}")
