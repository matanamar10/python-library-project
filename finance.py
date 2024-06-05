from pydantic import BaseModel
from datetime import datetime
import logging


# finance.py

# The patron class is an abstract class. Student and Teacher class going to inherit from this one.
def calculate_bill(patron):
    calculated_bill = 0
    check_date = datetime.now()
    for patron_item_isbn, patron_item_due_date in patron.patron_items():
        if check_date > patron_item_due_date:
            days_late = (check_date - patron_item_due_date).days
            fine = days_late * 0.50  # Example fine calculation: $0.50 per day late
            calculated_bill = calculated_bill + fine
        else:
            logging.info(f"There isn't any bill to add for this book!")
    return calculated_bill


class Finance(BaseModel):
    pass
