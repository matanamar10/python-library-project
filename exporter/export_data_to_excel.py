from library_system.patrons.students import Student
from library_system.library_items.disks.disks import Disk

DISK_TYPE = "Disk"
BOOK_TYPE = "Book"
STUDENT_TYPE = "Student"
TEACHER_TYPE = "Teacher"


def export_data(data, filename, headers, row_preparer):
    """
    Export data to a CSV file.

    :param data: Dictionary containing the data to be exported
    :param filename: Name of the CSV file
    :param headers: List of headers for the CSV file
    :param row_preparer: Function to prepare each row for the CSV file
    """
    import csv

    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)

        for key, value in data.items():
            row = row_preparer(key, value)
            writer.writerow(row)


def item_row_preparer(k, v):
    return [k, DISK_TYPE if isinstance(v, Disk) else BOOK_TYPE, v.title, v.is_borrowed]


def patron_row_preparer(k, v):
    return [k, STUDENT_TYPE if isinstance(v, Student) else TEACHER_TYPE, v.name, list(v.patron_items.items())]


def bill_row_preparer(k, v):
    return [k, v]
