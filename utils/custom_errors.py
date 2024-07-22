# custom_errors.py

class LibraryError(Exception):
    """Base class for all library-related errors."""

    def __init__(self, message=None):
        if message is None:
            self.message = "Library error occurred"
        super().__init__(message)


class ItemAlreadyExistsError(LibraryError):
    """Raised when a library item already exists."""

    def __init__(self, item_isbn: str):
        message = f"The library item with isbn {item_isbn} is already exist in the library system"
        super().__init__(message)


class PatronAlreadyExistsError(LibraryError):
    """Raised when a library item already exists."""

    def __init__(self, patron_id: str):
        message = f"The library patron with id {patron_id} is already exist in the library system"
        super().__init__(message)


class LibraryItemNotFoundError(LibraryError):
    """Raised when a library item not found in the library system."""

    def __init__(self, item_isbn: str):
        message = f"The library item with isbn {item_isbn} is not found in the library system"
        super().__init__(message)


class LibraryItemAlreadyBorrowedError(LibraryError):
    """Raised when a library item is already borrowed."""

    def __init__(self, item_isbn: str):
        message = f"The library item with isbn {item_isbn} is already marked as borrowed "
        super().__init__(message)


class PatronNotFoundError(LibraryError):
    """Raised when a patron does not exist."""

    def __init__(self, patron_id: str):
        message = f"The patron with id {patron_id} is not found in the library system"
        super().__init__(message)


class BillToPayError(LibraryError):
    """Raised when a patron needs to pay their bills before they can perform an action on library items."""

    def __init__(self, patron_id: str):
        message = f"The patron with id {patron_id} need to pay his bills before he can borrow/return a book"
        super().__init__(message)


class BorrowedLibraryItemNotFound(LibraryError):
    """Raised when a patron try to return an item which is not marked as borrowed."""

    def __init__(self, item_isbn: str):
        message = f"The libray item with isbn {item_isbn} is exist but he is not borrowed."
        super().__init__(message)
