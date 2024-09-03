# utils/custom_library_errors.py

class LibraryError(Exception):
    """Base class for all library-related errors."""

    def __init__(self, message=None, status_code=400):
        self.status_code = status_code
        if message is None:
            message = "Library error occurred"
        super().__init__(message)
        self.message = message


class ItemAlreadyExistsError(LibraryError):
    """Raised when a library item already exists."""

    def __init__(self, item_isbn: str):
        message = f"The library item with ISBN {item_isbn} already exists in the library system."
        super().__init__(message, status_code=400)


class PatronAlreadyExistsError(LibraryError):
    """Raised when a library patron already exists."""

    def __init__(self, patron_id: str):
        message = f"The library patron with ID {patron_id} already exists in the library system."
        super().__init__(message, status_code=400)


class LibraryItemNotFoundError(LibraryError):
    """Raised when a library item is not found in the library system."""

    def __init__(self, item_isbn: str):
        message = f"The library item with ISBN {item_isbn} is not found in the library system."
        super().__init__(message, status_code=404)


class LibraryItemAlreadyBorrowedError(LibraryError):
    """Raised when a library item is already borrowed."""

    def __init__(self, item_isbn: str):
        message = f"The library item with ISBN {item_isbn} is already marked as borrowed."
        super().__init__(message, status_code=400)


class PatronNotFoundError(LibraryError):
    """Raised when a patron does not exist."""

    def __init__(self, patron_id: str):
        message = f"The patron with ID {patron_id} is not found in the library system."
        super().__init__(message, status_code=404)


class BillToPayError(LibraryError):
    """Raised when a patron needs to pay their bills before they can perform an action on library items."""

    def __init__(self, patron_id: str):
        message = f"The patron with ID {patron_id} needs to pay their bills before borrowing/returning a book."
        super().__init__(message, status_code=403)


class BorrowedLibraryItemNotFound(LibraryError):
    """Raised when a patron tries to return an item that is not marked as borrowed."""

    def __init__(self, item_isbn: str):
        message = f"The library item with ISBN {item_isbn} exists but is not marked as borrowed."
        super().__init__(message, status_code=404)
