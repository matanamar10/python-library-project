from pydantic import BaseModel
from datetime import datetime
import logging

"""The finance class is take care all the finance side in the library - 
in our case is for right now to calculate the bills for students/teachers that late in returning borrowed items.
"""

"""The calculate bill function calculate the bill for the relevant patron
The function get :
1. patron - the patron object - and on him it will calculate the bill"""


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


"""The function return the calculated bill"""


class Finance(BaseModel):
    pass
