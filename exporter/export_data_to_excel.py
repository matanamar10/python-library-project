import csv
from typing import Dict, Any, Callable, List
from library_system.library_items.disks.disks import Disk
from library_system.patrons.students import Student

# Constants for file paths
LIBRARY_ITEMS_FILE = 'data/library_items.csv'
PATRONS_FILE = 'data/patrons.csv'
BILLS_FILE = 'data/bills.csv'


def export_to_csv(data: Dict[str, Any], filename: str, headers: List[str],
                  row_preparer: Callable[[str, Any], List[Any]]):
    """
    A generic function to export data to a CSV file.

    :param data: The dictionary containing the data to export.
    :param filename: The path of the CSV file to write.
    :param headers: The headers for the CSV file.
    :param row_preparer: A function to prepare each row for the CSV file.
    """
    with open(filename, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for key, value in data.items():
            writer.writerow(row_preparer(key, value))


# Example row preparer functions
def prepare_library_item_row(isbn: str, item: Any) -> List[Any]:
    """Prepare a row for a library item."""
    return [isbn, "Disk" if isinstance(item, Disk) else "Book", item.title, item.is_borrowed]


def prepare_patron_row(id: str, patron: Any) -> List[Any]:
    """Prepare a row for a patron."""
    return [id, "Student" if isinstance(patron, Student) else "Teacher", patron.name, list(patron.patron_items.items())]


def prepare_bill_row(student_id: str, bill: float) -> List[Any]:
    """Prepare a row for a bill."""
    return [student_id, bill]
