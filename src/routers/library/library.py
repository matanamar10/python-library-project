from typing import Dict, List

from src.models.requests.patrons.patron import AddPatronsRequest
from fastapi import APIRouter, Depends
from src.models.requests.library_items.items import AddItemsRequest
from src.models.responses.library_items.items import LibraryItemResponse, NewItemsResponse, LibraryItemStatusResponse
from src.models.responses.patrons.patron import PatronResponse, LibraryPatronStatusResponse, NewPatronsResponse
from src.dependencies import get_library

library_router = APIRouter()


@library_router.post(path="/items", response_model=NewItemsResponse, tags=["Library Items"])
async def add_items(add_new_items_request: AddItemsRequest, library=Depends(get_library)):
    """
    Add new items to the library asynchronously.
    """
    await library.add_items(new_library_items=add_new_items_request.library_items)
    return NewItemsResponse(
        message=f"New items {add_new_items_request.library_items} have been successfully added to the library collection.",
    )


@library_router.post(path="/patrons", response_model=NewPatronsResponse, tags=["Library Patrons"])
async def add_patrons(add_new_patrons_request: AddPatronsRequest, library=Depends(get_library)):
    """
    Add new patrons to the library asynchronously.
    """
    await library.add_new_patron_to_the_library(patrons_to_add=add_new_patrons_request.patrons_to_add)
    return {
        "message": f"The new patrons {add_new_patrons_request.patrons_to_add} successfully added"
    }


@library_router.delete(path="/patrons/{id}", response_model=LibraryPatronStatusResponse, tags=["Library Patrons"])
async def delete_patron(patron_id: str, library=Depends(get_library)):
    """
    Delete a patron from the library asynchronously.
    """
    await library.remove_patron(patron_id=patron_id)
    return {
        "message": "Patron successfully removed",
        "patron id": patron_id
    }


@library_router.delete(path="/items/{item_isbn}", response_model=LibraryItemStatusResponse, tags=["Library Items"])
async def delete_item(item_isbn: str, library=Depends(get_library)):
    """
    Delete an item from the library asynchronously.
    """
    await library.remove_item(item_isbn_to_remove=item_isbn)
    return {
        "message": "Item successfully removed from the library",
        "isbn": item_isbn
    }


@library_router.get(path="/items/{isbn}", response_model=LibraryItemResponse, tags=["Library Items"])
async def get_item(item_isbn: str, library=Depends(get_library)):
    """
    Get details of a library item asynchronously.
    """
    item = await library.get_item(item_isbn)
    return {"item": item}


@library_router.get(path="/patrons/{id}", response_model=PatronResponse, tags=["Library Patrons"])
async def get_patron(patron_id: str, library=Depends(get_library)):
    """
    Get details of a library patron asynchronously.
    """
    patron = await library.get_patron(patron_id)
    return {"patron": patron}


@library_router.get("/search", response_model=List[LibraryItemResponse], tags=["Library Items"])
async def search_library_items(criteria: Dict[str, str], library=Depends(get_library)):
    """
    Search for library items asynchronously based on criteria.
    """
    items = await library.search_items(criteria)
    return items
