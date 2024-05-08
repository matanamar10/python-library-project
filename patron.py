# patron.py
from utils import contain_non_letters


# The patron class is an abstract class. Student and Teacher class going to inherit from this one.
class Patron:
    def __init__(self, name, patron_id):
        self.name = name
        self.patron_id = patron_id

    """Function to check if there is a problem with the patron details"""
    def verify_patron_details(self):
        # Error handling - Check Verification : don't contain non-letters & id digit numbers is nine exact!
        try:
            if contain_non_letters(self.name):
                raise ValueError(f"The patron name you provided contains non-letter characters - fix it!")
            elif len(self.patron_id) != 9:
                raise ValueError(f"The patron id number must be 9 digits exact!")
            return True
        except ValueError as e:
            print(f"patron details verification failed due to unexpected errors {e}")
            return False