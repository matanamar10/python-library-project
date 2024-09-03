from src.models.requests.patrons.patron import AddPatronsRequest
from fastapi import APIRouter, Depends
from src.models.requests.library_items.items import *
from src.models.responses.patrons.patron import *
from src.models.responses.library_items.items import *
from src.dependencies import get_library
from src.models.responses.patrons.patron import LibraryPatronStatusResponse, PatronResponse

library_router = APIRouter()


@library_router.post(path="/items", response_model=NewItemsResponse, tags=["Library Items"])
def add_item(add_new_item_request: AddItemRequest, library=Depends(get_library)):
    """
    Add new items to the library.

    This endpoint allows you to add new items (e.g., books, disks) to the library's collection.
    The items to be added are provided in the request body.

    Args:
        add_new_item_request (AddItemRequest): A request object containing the details of the items to be added.
        library: The library instance, injected via dependency.

    Returns:
        dict: A message confirming the successful addition of the new items.
    """
    library.add_items(new_library_items=add_new_item_request.library_items)
    return {
        "message": "The new items successfully added"
    }


@library_router.post(path="/patrons", response_model=NewPatronsResponse, tags=["Library Patrons"])
def add_patrons(add_new_patrons_request: AddPatronsRequest, library=Depends(get_library)):
    """
    Add new patrons to the library.

    This endpoint allows you to add new patrons to the library's system.
    The patrons to be added are provided in the request body.

    Args:
        add_new_patrons_request (AddPatronsRequest): A request object containing the details of the patrons to be added.
        library: The library instance, injected via dependency.

    Returns:
        dict: A message confirming the successful addition of the new patrons.
    """
    library.add_new_patron_to_the_library(patrons_to_add=add_new_patrons_request.patrons_to_add)
    return {
        "message": "The new patrons successfully added"
    }


@library_router.delete(path="/patrons/{id}", response_model=LibraryPatronStatusResponse, tags=["Library Patrons"])
def delete_patron(patron_id: str, library=Depends(get_library)):
    """
    Delete a patron from the library.

    This endpoint allows you to remove a patron from the library's system using their ID.

    Args:
        patron_id (str): The ID of the patron to be removed.
        library: The library instance, injected via dependency.

    Returns:
        dict: A message confirming the successful removal of the patron, along with the patron's ID.
    """
    library.remove_patron(patron_id=patron_id)
    return {
        "message": "Patron successfully removed",
        "patron id": patron_id
    }


@library_router.delete(path="/items/{item_isbn}", response_model=LibraryItemStatusResponse, tags=["Library Items"])
def delete_item(item_isbn: str, library=Depends(get_library)):
    """
    Delete an item from the library.

    This endpoint allows you to remove an item from the library's collection using its ISBN.

    Args:
        item_isbn (str): The ISBN of the item to be removed.
        library: The library instance, injected via dependency.

    Returns:
        dict: A message confirming the successful removal of the item, along with the item's ISBN.
    """
    library.remove_item(item_isbn_to_remove=item_isbn)
    return {
        "message": "Item successfully removed from the library",
        "isbn": item_isbn
    }


@library_router.get(path="/items/{isbn}", response_model=LibraryItemResponse, tags=["Library Items"])
def get_item(item_isbn: str, library=Depends(get_library)):
    """
    Get details of a library item.

    This endpoint retrieves the details of a specific library item using its ISBN.

    Args:
        item_isbn (str): The ISBN of the item to retrieve.
        library: The library instance, injected via dependency.

    Returns:
        dict: A dictionary containing the details of the requested library item.
    """
    item = library.items[item_isbn]
    return {"item": item}


@library_router.get(path="/patrons/{id}", response_model=PatronResponse, tags=["Library Patrons"])
def get_patron(patron_id: str, library=Depends(get_library)):
    """
    Get details of a library patron.

    This endpoint retrieves the details of a specific patron using their ID.

    Args:
        patron_id (str): The ID of the patron to retrieve.
        library: The library instance, injected via dependency.

    Returns:
        dict: A dictionary containing the details of the requested patron.
    """
    patron = library.patrons[patron_id]
    return {"patron": patron}
