import re


# Function to check if strings contains non-letters chars inside.
def contain_non_letters(string):
    pattern = re.compile(r'[^a-zA-Z\s]')
    return bool(pattern.search(string))

