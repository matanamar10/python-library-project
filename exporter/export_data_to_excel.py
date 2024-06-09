import csv
from typing import Dict, Any
from library_objects.students import Student
from library_objects.disks import Disk


def export_library_attributes(data: Dict[str, Any], attribute_type: str):
    """
    A generic function to export different library attributes to a CSV file based on the attribute_type.

    :param data: The dictionary containing the data to export.
    :param attribute_type: Type of attribute to export ('items', 'patrons', 'bills').
    """
    export_config = {
        'items': {
            'filename': 'library_items.csv',
            'headers': ["ISBN", "Type", "Title", "Is Borrowed?"],
            'row_preparer': lambda k, v: [k, "Disk" if isinstance(v, Disk) else "Book", v.title, v.is_borrowed]
        },
        'patrons': {
            'filename': 'patrons.csv',
            'headers': ["ID", "Type", "Name", "Library-Items"],
            'row_preparer': lambda k, v: [k, "Student" if isinstance(v, Student) else "Teacher", v.name,
                                          list(v.patron_items.items())]
        },
        'bills': {
            'filename': 'bills.csv',
            'headers': ["Student ID", "Calculated Bill"],
            'row_preparer': lambda k, v: [k, v]
        }
    }

    if attribute_type not in export_config:
        raise ValueError(f"Unknown attribute_type: {attribute_type}")

    config = export_config[attribute_type]
    filename = config['filename']
    headers = config['headers']
    row_preparer = config['row_preparer']

    with open(filename, mode="w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        for key, value in data.items():
            writer.writerow(row_preparer(key, value))
