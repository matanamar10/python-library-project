import csv
from students import Student
from disks import Disk
from pydantic import BaseModel

"""The DataExporter class will take care in any data exporting of the library data We chose to export all the library 
data to separated excel files. Each time that there is a change in one of the Library classes methods - this class 
methods will be called - each by his responsibility"""

"""The export_library_items method being called every time there is a change in the library items - book or disks
it could be deletion of the items from the library system or status changing of the items itself - for example: 
if customer return a book - it not borrowed anymore.

The method get as parameters:
1.The library items dict from the library itself."""


def export_library_items(library_items):
    with open("library_items.csv", mode="w", newline='') as library_items_file:
        library_items_writer = csv.writer(library_items_file)
        library_items_writer.writerow(["ISBN", "Type", "Title", "Is Borrowed?"])
        for library_item_isbn, library_item in library_items.items():
            library_item_type = "Disk" if isinstance(library_item, Disk) else "Book"
            library_items_writer.writerow(
                [library_item_isbn, library_item_type, library_item.title, library_item.is_borrowed])


"""The export_library_patrons method being called every time there is a change in the library patrons - students or 
teachers it could be deletion of the items from the library system or status changing of the items itself
 - for example: 
if student return a book - it not assign to him anymore.

The method get as parameters:
1.The library_patrons dict from the library itself."""


def export_library_patrons(library_patrons):
    with open("patrons.csv", mode="w", newline='') as patrons_file:
        patrons_writer = csv.writer(patrons_file)
        patrons_writer.writerow(["ID", "Type", "Name", "Library-Items"])
        for patron_id, patron in library_patrons.items():
            patron_type = "Student" if isinstance(patron, Student) else "Teacher"
            patrons_writer.writerow([patron_type, patron_type, patron.name, list(patron.patron_items.items())])


"""The export_bills method being called every time there is a change in the library bills system - for example: 
if student return a book - it will check if he got a bills to pay and if he got - 
it will call the export_bills method.

The method get as parameters:
1.The library_bills dict from the library itself."""


def export_bills(library_bills):
    with open("bills.csv", mode="w", newline='') as bills_file:
        bills_writer = csv.writer(bills_file)
        bills_writer.writerow(["Student ID", "Calculated Bill"])
        for patron_id, bill in library_bills.items():
            bills_writer.writerow([patron_id, bill])


class DataExporter(BaseModel):
    pass
