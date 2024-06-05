import csv
from students import Student
from disks import Disk
from pydantic import BaseModel


def export_library_items(library_items):
    with open("library_items.csv", mode="w", newline='') as library_items_file:
        library_items_writer = csv.writer(library_items_file)
        library_items_writer.writerow(["ISBN", "Type", "Title", "Is Borrowed?"])
        for library_item_isbn, library_item in library_items.items():
            library_item_type = "Disk" if isinstance(library_item, Disk) else "Book"
            library_items_writer.writerow(
                [library_item_isbn, library_item_type, library_item.title, library_item.is_borrowed])


def export_library_patrons(library_patrons):
    with open("patrons.csv", mode="w", newline='') as patrons_file:
        patrons_writer = csv.writer(patrons_file)
        patrons_writer.writerow(["ID", "Type", "Name", "Library-Items"])
        for patron_id, patron in library_patrons.items():
            patron_type = "Student" if isinstance(patron, Student) else "Teacher"
            patrons_writer.writerow([patron_type, patron_type, patron.name, list(patron.patron_items.items())])


def export_bills(library_bills):
    with open("bills.csv", mode="w", newline='') as bills_file:
        bills_writer = csv.writer(bills_file)
        bills_writer.writerow(["Student ID", "Calculated Bill"])
        for patron_id, bill in library_bills.items():
            bills_writer.writerow([patron_id, bill])


class DataExporter(BaseModel):
    pass
