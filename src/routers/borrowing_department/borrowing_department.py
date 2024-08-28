# routers/borrowing_department.py

from fastapi import APIRouter, Depends
from src.models.responses.library_items.items import LibraryItemStatusResponse
from src.models.requests.library_items.items import BorrowRequest
from src.dependencies import get_library, get_borrowing_department
from src.models.responses.patrons.patron import LibraryPatronStatusResponse

borrowing_department_router = APIRouter()


@borrowing_department_router.patch("/return", response_model=LibraryPatronStatusResponse, tags=["Borrowing Department"])
def return_item(borrow_request: BorrowRequest,
                borrowing_department=Depends(get_borrowing_department)):
    """
    Return a borrowed library item.

    This endpoint allows a patron to return a previously borrowed item to the library.
    The borrowing department processes the return and updates the patron's borrowing status.

    Args:
        borrow_request (BorrowRequest): Contains the details of the library item and patron ID.
        borrowing_department: Dependency injection of the borrowing department for managing item returns.

    Returns:
        dict: A dictionary containing a success message and the updated status of the patron.
    """

    patron = borrowing_department.return_item(
        library_item=borrow_request.library_item,
        patron_id=borrow_request.patron_id
    )
    return {
        "message": "Item successfully returned",
        "patron": {"patron": patron}
    }


@borrowing_department_router.patch("/borrow", response_model=LibraryItemStatusResponse, tags=["Borrowing Department"])
def borrow_item(borrow_request: BorrowRequest,
                borrowing_department=Depends(get_borrowing_department)):
    """
    Borrow a library item.

    This endpoint allows a patron to borrow an item from the library.
    The borrowing department processes the borrowing request and updates the item's status.

    Args:
        borrow_request (BorrowRequest): Contains the details of the library item and patron ID.
        borrowing_department: Dependency injection of the borrowing department for managing item borrowing.

    Returns:
        dict: A dictionary containing a success message and the updated status of the library item.
    """

    item = borrowing_department.borrow_library_item(
        library_item=borrow_request.library_item,
        patron_id=borrow_request.patron_id
    )
    return {
        "message": "Item successfully borrowed",
        "item": {"item": item}
    }
