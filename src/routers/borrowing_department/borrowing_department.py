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
    item = borrowing_department.borrow_library_item(
        library_item=borrow_request.library_item,
        patron_id=borrow_request.patron_id
    )
    return {
        "message": "Item successfully borrowed",
        "item": {"item": item}
    }
