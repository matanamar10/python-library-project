# routers/borrowing_department.py

from fastapi import APIRouter, Depends
from src.models.responses.library_items.items import LibraryItemStatusResponse
from src.models.requests.library_items.items import BorrowRequest
from src.dependencies import get_library, get_borrowing_department

borrowing_department_router = APIRouter()


@borrowing_department_router.put("/borrow", response_model=LibraryItemStatusResponse, tags=["Borrowing Department"])
def borrow_item(borrow_request: BorrowRequest, library=Depends(get_library),
                borrowing_department=Depends(get_borrowing_department)):
    borrowing_department.borrow_library_item(
        library=library,
        library_item=borrow_request.library_item,
        patron_id=borrow_request.patron_id
    )
    return {"message": "Item successfully borrowed"}


@borrowing_department_router.put("/return", response_model=LibraryItemStatusResponse, tags=["Borrowing Department"])
def return_item(borrow_request: BorrowRequest, library=Depends(get_library),
                borrowing_department=Depends(get_borrowing_department)):
    borrowing_department.return_library_item(
        library=library,
        library_item=borrow_request.library_item,
        patron_id=borrow_request.patron_id
    )
    return {"message": "Item successfully returned"}
