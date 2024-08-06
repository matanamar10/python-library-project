# routers/items.py

from fastapi import APIRouter, HTTPException, Depends
from controllers.library import Library
from models.entities.library_items import LibraryItem
from utils.custom_library_errors import LibraryError
from src.dependencies import get_library

library_items_router = APIRouter()


@library_items_router.post("/", response_model=LibraryItem)
def add_item(item: LibraryItem, library: Library = Depends(get_library)):
    try:
        library.add_item(item)
        return item
    except LibraryError as e:
        raise HTTPException(status_code=400, detail=str(e))


@library_items_router.get("/", response_model=list[LibraryItem])
def get_items(library: Library = Depends(get_library)):
    return library.get_all_items()


@library_items_router.get("/{isbn}", response_model=LibraryItem)
def get_item(isbn: str, library: Library = Depends(get_library)):
    try:
        return library.get_item(isbn)
    except LibraryError as e:
        raise HTTPException(status_code=404, detail=str(e))


@library_items_router.delete("/{isbn}")
def delete_item(isbn: str, library: Library = Depends(get_library)):
    try:
        library.remove_item(isbn)
        return {"detail": "Item deleted successfully"}
    except LibraryError as e:
        raise HTTPException(status_code=400, detail=str(e))
