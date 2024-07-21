# custom_errors.py

class LibraryError(Exception):
    """Base class for all library-related errors."""
    pass


class NotUniqueLibraryItemError(LibraryError):
    """Raised when a library item already exists."""
    pass


class NotUniquePatronError(LibraryError):
    """Raised when a library patron already exists."""
    pass


class LibraryItemDoesNotExistError(LibraryError):
    """Raised when a library item does not exist."""
    pass


class LibraryItemBorrowedError(LibraryError):
    """Raised when a library item is already borrowed."""
    pass


class PatronDoesNotExistError(LibraryError):
    """Raised when a patron does not exist."""
    pass


class MultipleRecordsFoundError(LibraryError):
    """Raised when multiple records are found."""
    pass


class DatabaseOperationError(LibraryError):
    """Raised when there is a database operation error."""
    pass


class ValidationError(LibraryError):
    """Raised when there is a validation error."""
    pass


class OutstandingBillError(LibraryError):
    """Raised when a patron has an outstanding bill."""
    pass


class NotExistingPatron(LibraryError):
    """Raised when a patron which not exist in the library system try to perform actions."""
    pass


class NotExistingLibraryItem(LibraryError):
    """Raised when a library item which is not exist in the library system wants to be returned or borrowed."""
    pass


class ExistingBillToPay(LibraryError):
    """Raised when a patron needs to pay their bills before they can perform an action on library items."""
    pass


class NotBorrowedLibraryItem(LibraryError):
    """Raised when a patron try to return a item which is not marked as borrowed."""
    pass


class BorrowedLibraryItem(LibraryError):
    """Raised when a patron try to borrow a library item which is already borrowed"""
    pass
