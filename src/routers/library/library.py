from src.models.requests.patrons.patron import AddPatronsRequest
from fastapi import APIRouter, Depends
from src.models.responses.library_items.items import LibraryItemStatusResponse, LibraryItemResponse, NewItemsResponse, \
    NewPatronsResponse
from src.models.requests.library_items.items import AddItemRequest
from src.dependencies import get_library
from src.models.responses.patrons.patron import LibraryPatronStatusResponse, PatronResponse

library_router = APIRouter()


@library_router.post(path="/items", response_model=NewItemsResponse, tags=["Library Items"])
def add_library_item(add_new_item_request: AddItemRequest, library=Depends(get_library)):
    library.add_new_library_items_to_the_library(new_library_items=add_new_item_request.library_items)
    return {
        "message": "The new items successfully added"
    }


@library_router.post(path="/patrons", response_model=NewPatronsResponse, tags=["Library Patrons"])
def add_patrons(add_new_patrons_request: AddPatronsRequest, library=Depends(get_library)):
    library.add_new_patron_to_the_library(patrons_to_add=add_new_patrons_request.patrons_to_add)
    return {
        "message": "The new patrons successfully added"
    }


@library_router.delete(path="/patrons/{id}", response_model=LibraryPatronStatusResponse,
                       tags=["Library Patrons"])
def delete_patrons(patron_id: str, library=Depends(get_library)):
    library.remove_patrons_from_the_library(patron_id=patron_id)
    return {
        "message": "Patron successfully removed",
        "patron id": patron_id
    }


@library_router.delete(path="/items/{item_isbn}", response_model=LibraryItemStatusResponse, tags=["Library Items"])
def delete_items(item_isbn: str, library=Depends(get_library)):
    library.remove_items_from_the_library(item_isbn_to_remove=item_isbn)
    return {
        "message": "Item successfully removed from the library",
        "isbn": item_isbn
    }


@library_router.get(path="/items/{isbn}", response_model=LibraryItemResponse, tags=["Library Items"])
def get_library_item(item_isbn: str, library=Depends(get_library)):
    item = library.library_items[item_isbn]
    return {"item": item}


@library_router.get(path="/patrons/{id}", response_model=PatronResponse, tags=["Library Patrons"])
def get_library_patron(patron_id: str, library=Depends(get_library)):
    patron = library.patrons[patron_id]
    return {"patron": patron}
