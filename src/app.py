import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.controllers.library import Library
from src.controllers.management.borrowing_department import BorrowingDepartment
from src.routers.borrowing_department.borrowing_department import borrowing_department_router
from src.routers.library.library import library_router
from utils.custom_library_errors import LibraryError


def create_app(library_name: str) -> FastAPI:
    app = FastAPI()
    app.state.library = Library(name=library_name)
    app.state.borrowing_department = BorrowingDepartment()
    app.include_router(library_router, prefix="/library")
    app.include_router(borrowing_department_router, prefix="/borrowing")

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    @app.exception_handler(LibraryError)
    async def library_error_exception_handler(request: Request, exc: LibraryError):
        logging.error(f"Error on {request.url.path}: {exc}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": str(exc)},
        )

    return app
