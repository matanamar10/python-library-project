# src/app.py

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from src.controllers.library import Library
from src.controllers.management.borrowing_department import BorrowingDepartment
from src.routers.borrowing_department.borrowing_department import borrowing_department_router
from src.routers.library.library import library_router
from utils.custom_library_errors import PatronNotFoundError, LibraryItemNotFoundError, LibraryItemAlreadyBorrowedError


def create_app(library_name: str) -> FastAPI:
    app = FastAPI()

    # Initialize and store the Library instance in the app's state
    app.state.library = Library(name=library_name)

    app.state.borrowing_department = BorrowingDepartment()

    # Include routers
    app.include_router(library_router, prefix="/library")
    app.include_router(borrowing_department_router, prefix="/borrowing")

    @app.exception_handler(PatronNotFoundError)
    async def patron_not_found_exception_handler(request: Request, exc: PatronNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(LibraryItemNotFoundError)
    async def library_item_not_found_exception_handler(request: Request, exc: LibraryItemNotFoundError):
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(LibraryItemAlreadyBorrowedError)
    async def library_item_already_borrowed_exception_handler(request: Request, exc: LibraryItemAlreadyBorrowedError):
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    return app
