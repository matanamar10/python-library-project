import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.controllers.library import Library
from src.controllers.management.borrowing_department import BorrowingDepartment
from src.routers.borrowing_department.borrowing_department import borrowing_department_router
from src.routers.library.library import library_router
from utils.custom_library_errors import (
    PatronNotFoundError,
    LibraryItemNotFoundError,
    LibraryItemAlreadyBorrowedError,
    BorrowedLibraryItemNotFound,
    BillToPayError,
    PatronAlreadyExistsError,
    ItemAlreadyExistsError
)


def create_app(library_name: str) -> FastAPI:
    app = FastAPI()

    # Initialize and store the Library instance in the app's state
    app.state.library = Library(name=library_name)
    app.state.borrowing_department = BorrowingDepartment()

    # Include routers
    app.include_router(library_router, prefix="/library")
    app.include_router(borrowing_department_router, prefix="/borrowing")

    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Exception Handlers with Logging
    @app.exception_handler(ItemAlreadyExistsError)
    async def item_already_exists_exception_handler(request: Request, exc: ItemAlreadyExistsError):
        logging.error(f"Error on {request.url.path}: {exc}")
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(PatronAlreadyExistsError)
    async def patron_already_exists_exception_handler(request: Request, exc: PatronAlreadyExistsError):
        logging.error(f"Error on {request.url.path}: {exc}")
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(LibraryItemNotFoundError)
    async def library_item_not_found_exception_handler(request: Request, exc: LibraryItemNotFoundError):
        logging.error(f"Error on {request.url.path}: {exc}")
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(LibraryItemAlreadyBorrowedError)
    async def library_item_already_borrowed_exception_handler(request: Request, exc: LibraryItemAlreadyBorrowedError):
        logging.error(f"Error on {request.url.path}: {exc}")
        return JSONResponse(
            status_code=400,
            content={"detail": str(exc)},
        )

    @app.exception_handler(PatronNotFoundError)
    async def patron_not_found_exception_handler(request: Request, exc: PatronNotFoundError):
        logging.error(f"Error on {request.url.path}: {exc}")
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    @app.exception_handler(BillToPayError)
    async def bill_to_pay_exception_handler(request: Request, exc: BillToPayError):
        logging.error(f"Error on {request.url.path}: {exc}")
        return JSONResponse(
            status_code=403,
            content={"detail": str(exc)},
        )

    @app.exception_handler(BorrowedLibraryItemNotFound)
    async def borrowed_library_item_not_found_exception_handler(request: Request, exc: BorrowedLibraryItemNotFound):
        logging.error(f"Error on {request.url.path}: {exc}")
        return JSONResponse(
            status_code=404,
            content={"detail": str(exc)},
        )

    return app
