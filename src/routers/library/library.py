from src.models.requests.patrons.patron import AddPatronsRequest, PatronRequest
from fastapi import APIRouter, Depends
from src.models.responses.library_items.items import LibraryItemStatusResponse, LibraryItemResponse
from src.models.requests.library_items.items import AddItemRequest, SearchItemsRequest, ItemRequest
from src.dependencies import get_library
from src.models.responses.patrons.patron import LibraryPatronStatusResponse

library_router = APIRouter()


@library_router.post(path="/items", response_model=LibraryItemStatusResponse, tags=["Library Items"])
def add_library_item(add_new_item_request: AddItemRequest, library=Depends(get_library)):
    items = library.add_new_library_items_to_the_library(new_library_items=add_new_item_request.library_items)
    return {
        "message": "The new items successfully added",
        "item": {"item": items[0]}  # Assuming adding multiple items, return the first one
    }


@library_router.post(path="/patrons", response_model=LibraryPatronStatusResponse, tags=["Library Patrons"])
def add_patrons(add_new_patrons_request: AddPatronsRequest, library=Depends(get_library)):
    patrons = library.add_new_patron_to_the_library(patrons_to_add=add_new_patrons_request.patrons_to_add)
    return {
        "message": "The new patrons successfully added",
        "patron": {"patron": patrons[0]}  # Assuming adding multiple patrons, return the first one
    }


@library_router.delete(path="/patrons/{patron_id}", response_model=LibraryPatronStatusResponse,
                       tags=["Library Patrons"])
def delete_patrons(remove_patrons_request: PatronRequest, library=Depends(get_library)):
    patron = library.remove_patrons_from_the_library(patrons_to_remove=remove_patrons_request.patrons_to_remove)
    return {
        "message": "Patron successfully removed",
        "patron": {"patron": patron}
    }


@library_router.get(path="/items", tags=["Library Items"])
def search_library_items(search_library_items_request: SearchItemsRequest, library=Depends(get_library)):
    items = library.search_library_items(
        library_item_title=search_library_items_request.library_item_title,
        library_item_isbn=search_library_items_request.library_item_isbn
    )
    return items


@library_router.delete(path="/items/{item_isbn}", response_model=LibraryItemStatusResponse, tags=["Library Items"])
def delete_items(remove_item_request: ItemRequest, library=Depends(get_library)):
    item = library.remove_items_from_the_library(item_isbn_to_remove=remove_item_request.library_item_isbn)
    return {
        "message": "Item successfully removed from the library",
        "item": {"item": item}
    }


@library_router.get(path="/items/{item_isbn}", response_model=LibraryItemResponse, tags=["Library Items"])
def get_library_item(get_item_request: ItemRequest, library=Depends(get_library)):
    item = library.library_items[get_item_request.item_isbn]
    return {"item": {"item": item}}


@library_router.get(path="/patrons/{id}", response_model=LibraryPatronStatusResponse, tags=["Library Patrons"])
def get_library_patron(get_patron_request: PatronRequest, library=Depends(get_library)):
    patron = library.patrons[get_patron_request.patron_id]
    return {"patron": {"patron": patron}}
