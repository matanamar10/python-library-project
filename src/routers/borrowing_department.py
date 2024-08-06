# routers/borrowing_department.py

from fastapi import APIRouter, HTTPException, Depends
from models.responses.library_items.items import LibraryItemStatusResponse
from models.requests.library_items.items import LibraryItemRequest, BorrowRequest
from src.dependencies import get_library, get_borrowing_department

borrowing_department_router = APIRouter()


@borrowing_department_router.post("/borrow", response_model=LibraryItemStatusResponse)
def borrow_item(borrow_request: BorrowRequest, library=Depends(get_library),
                borrowing_department=Depends(get_borrowing_department)):
    borrowing_department.borrow_library_item(
        library=library,
        library_item=borrow_request.library_item,
        patron_id=borrow_request.patron_id
    )
    return {"message": "Item successfully borrowed"}


@borrowing_department_router.post("/return", response_model=LibraryItemStatusResponse)
def return_item(borrow_request: BorrowRequest, library=Depends(get_library),
                borrowing_department=Depends(get_borrowing_department)):
    borrowing_department.return_library_item(
        library=library,
        library_item=borrow_request.library_item,
        patron_id=borrow_request.patron_id
    )
    return {"message": "Item successfully returned"}
