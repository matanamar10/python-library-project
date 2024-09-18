from datetime import datetime
import logging
from src.mongodb.mongodb_models.patron_model import PatronDocument


def calculate_bill(patron: PatronDocument) -> float:
    """
    Calculate the bill for a patron based on overdue library items.

    Args:
        patron (PatronDocument): The patron document for whom to calculate the bill.

    Returns:
        float: The calculated bill amount.
    """
    calculated_bill = 0
    check_date = datetime.now()

    # Assuming `patron_items` in PatronDocument stores items as a dictionary where the key is the ISBN and value is the due date
    for patron_item_isbn, patron_item_due_date in patron.items.items():
        if check_date > patron_item_due_date:
            days_late = (check_date - patron_item_due_date).days
            # Assuming `patron.discount` exists in PatronDocument; you can adjust this according to your model
            fine = days_late * 0.50 * patron.discount
            calculated_bill += fine
        else:
            logging.info(f"There isn't any bill to add for this book!")

    return calculated_bill
