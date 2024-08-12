# src/app.py

from fastapi import FastAPI

from src.controllers.library import Library
from src.controllers.management.borrowing_department import BorrowingDepartment
from src.routers.borrowing_department.borrowing_department import borrowing_department_router
from src.routers.library.library import library_router


def create_app(library_name: str) -> FastAPI:
    app = FastAPI()

    # Initialize and store the Library instance in the app's state
    app.state.library = Library(name=library_name)

    app.state.borrowing_department = BorrowingDepartment()

    # Include routers
    app.include_router(library_router, prefix="/library")
    app.include_router(borrowing_department_router, prefix="/borrowing")

    return app
