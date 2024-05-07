import re


# Function to check if strings contains non-letters chars inside.
def contain_non_letters(string):
    pattern = re.compile(r'[^a-zA-Z\s]')
    return bool(pattern.search(string))


# Function which convert the argument to iterable
def convert_to_list(library_object):
    if not isinstance(library_object, list):
        library_object = [library_object]
    return library_object


# Function to check if element exist in a dict
def is_library_element_exists(dictionary, element_id):
    if element_id in dictionary:
        print(f"element already exist")
        return True
    else:
        print(f"element not exist yet")
        return False


# Function which add element to dict
def add_to_dict(dictionary, key, value):
    dictionary[key] = value
    return dictionary
