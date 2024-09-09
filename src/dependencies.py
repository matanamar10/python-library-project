# src/dependencies.py

from fastapi import Request
from src.controllers.library import Library
from src.controllers.management.borrowing_department import BorrowingDepartment


def get_library(request: Request) -> Library:
    return request.app.state.library


def get_borrowing_department(request: Request) -> BorrowingDepartment:
    return request.app.state.borrowing_department
