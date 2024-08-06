# routers/borrowing_department.py

from fastapi import APIRouter, HTTPException, Depends
from src.dependencies import get_library
from controllers.management.borrowing_department import *

borrowing_department_router = APIRouter()


@borrowing_department_router.post("/borrow")
def borrow_item(patron_id: str, isbn: str, library: Library = Depends(get_library)):
    try:
        return {"detail": "Item borrowed successfully"}
    except LibraryError as e:
        raise HTTPException(status_code=400, detail=str(e))


@borrowing_department_router.post("/return")
def return_item(patron_id: str, isbn: str, library: Library = Depends(get_library)):
    try:
        library.return_item(patron_id, isbn)
        return {"detail": "Item returned successfully"}
    except LibraryError as e:
        raise HTTPException(status_code=400, detail=str(e))
