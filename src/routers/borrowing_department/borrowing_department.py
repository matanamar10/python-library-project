# routers/borrowing_department.py

from fastapi import APIRouter, Depends
from src.models.responses.library_items.items import LibraryItemStatusResponse
from src.models.requests.library_items.items import BorrowRequest
from src.dependencies import get_borrowing_department

borrowing_department_router = APIRouter()


@borrowing_department_router.patch("/return", response_model=LibraryItemStatusResponse, tags=["Borrowing Department"])
async def return_item(borrow_request: BorrowRequest, borrowing_department=Depends(get_borrowing_department)):
    await borrowing_department.return_item(borrow_request.library_item, borrow_request.patron_id)
    return {
        "message": "Item successfully returned",
        "item": borrow_request.library_item
    }


@borrowing_department_router.patch("/borrow", response_model=LibraryItemStatusResponse, tags=["Borrowing Department"])
async def borrow_item(borrow_request: BorrowRequest, borrowing_department=Depends(get_borrowing_department)):
    await borrowing_department.borrow_item(borrow_request.library_item, borrow_request.patron_id)
    return {
        "message": "Item successfully borrowed",
        "item": borrow_request.library_item
    }
