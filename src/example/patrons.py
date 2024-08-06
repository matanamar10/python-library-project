# routers/patrons.py

from fastapi import APIRouter, HTTPException, Depends
from controllers.library import Library
from models.entities.patrons import Patron
from utils.custom_library_errors import LibraryError
from src.dependencies import get_library

patrons_router = APIRouter()


@patrons_router.post("/", response_model=Patron)
def add_patron(patron: Patron, library: Library = Depends(get_library)):
    try:
        library.add_patron(patron)
        return patron
    except LibraryError as e:
        raise HTTPException(status_code=400, detail=str(e))


@patrons_router.get("/", response_model=list[Patron])
def get_patrons(library: Library = Depends(get_library)):
    return library.get_all_patrons()


@patrons_router.get("/{patron_id}", response_model=Patron)
def get_patron(patron_id: str, library: Library = Depends(get_library)):
    try:
        return library.get_patron(patron_id)
    except LibraryError as e:
        raise HTTPException(status_code=404, detail=str(e))


@patrons_router.delete("/{patron_id}")
def delete_patron(patron_id: str, library: Library = Depends(get_library)):
    try:
        library.remove_patrons_from_the_library(patrons_to_remove=[library.patrons[patron_id]])
        return {"detail": "Patron deleted successfully"}
    except LibraryError as e:
        raise HTTPException(status_code=400, detail=str(e))
