from src.models.requests.patrons.patron import AddPatronsRequest, RemovePatronsRequest
from fastapi import APIRouter, Depends
from src.models.responses.library_items.items import LibraryItemStatusResponse
from src.models.requests.library_items.items import AddItemRequest, SearchItemsRequest, \
    RemoveItemRequest
from src.dependencies import get_library

library_router = APIRouter()


@library_router.post(path="/items", response_model=LibraryItemStatusResponse, tags=["Library Items"])
def add_library_item(add_new_item_request: AddItemRequest, library=Depends(get_library)):
    library.add_new_library_items_to_the_library(new_library_items=add_new_item_request.library_items)
    return {"message": "Item successfully added"}


@library_router.post(path="/patrons", response_model=LibraryItemStatusResponse, tags=["Library Patrons"])
def add_patrons(add_new_patrons_request: AddPatronsRequest, library=Depends(get_library)):
    library.add_new_patron_to_the_library(patrons_to_add=add_new_patrons_request.patrons_to_add)
    return {"message": "Item successfully added"}


@library_router.delete(path="/patrons", response_model=LibraryItemStatusResponse, tags=["Library Patrons"])
def delete_patrons(remove_patrons_request: RemovePatronsRequest, library=Depends(get_library)):
    library.remove_patrons_from_the_library(patrons_to_remove=remove_patrons_request.patrons_to_remove)
    return {"message": "Item successfully added"}


@library_router.get(path="/items", response_model=LibraryItemStatusResponse, tags=["Library Items"])
def get_library_items(search_library_items_request: SearchItemsRequest, library=Depends(get_library)):
    results = library.search_library_items(
        library_item_title=search_library_items_request.library_item_title,
        library_item_isbn=search_library_items_request.library_item_isbn
    )
    return results


@library_router.delete(path="/items", response_model=LibraryItemStatusResponse, tags=["Library Items"])
def delete_items(remove_item_request: RemoveItemRequest, library=Depends(get_library)):
    library.remove_patrons_from_the_library(item_isbn_to_remove=remove_item_request.library_item_isbn)
    return {"message": "Item successfully added"}
