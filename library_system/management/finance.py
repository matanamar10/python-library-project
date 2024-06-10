from datetime import datetime
import logging

from library_system.patrons.patron import Patron


def calculate_bill(patron: Patron):
    """
    Calculate the bill for a patron based on overdue library_items.

    Args:
        patron (Patron): The patron for whom to calculate the bill.

    Returns:
        float: The calculated bill amount.
    """

    calculated_bill = 0
    check_date = datetime.now()
    for patron_item_isbn, patron_item_due_date in patron.patron_items.items():
        if check_date > patron_item_due_date:
            days_late = (check_date - patron_item_due_date).days
            fine = days_late * 0.50 * patron.discount
            calculated_bill = calculated_bill + fine
        else:
            logging.info(f"There isn't any bill to add for this book!")
    return calculated_bill
