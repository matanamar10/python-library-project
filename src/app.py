# src/app.py

from fastapi import FastAPI
from controllers.library import Library
from controllers.management.borrowing_department import BorrowingDepartment
from src.routers import borrowing_department


def create_app(library_name: str) -> FastAPI:
    app = FastAPI()

    # Initialize and store the Library instance in the app's state
    app.state.library = Library(name=library_name)

    app.state.borrowing_department = BorrowingDepartment()

    # Include routers
    app.include_router(patrons.patrons_router, prefix="/patrons", tags=["Patrons"])
    app.include_router(library_items.library_items_router, prefix="/items", tags=["Items"])
    app.include_router(borrowing_department.borrowing_department_router, prefix="/borrowing", tags=["Borrowing"])

    return app
