import logging
from src.controllers.controllers_manager import ControllersManager
from src.models.entities.library_items.items import LibraryItem
from src.models.entities.patrons.patron import Patron
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument
from utils.utils import patron_pydantic_to_mongoengine, item_pydantic_to_mongoengine
from utils.custom_library_errors import *


class Library(BaseModel):
    items: Dict[str, LibraryItem] = {}
    patrons: Dict[str, Patron] = {}
    bills: Dict[str, float] = {}
    name: str
    controllers_manager: Optional[ControllersManager] = None

    class Config:
        arbitrary_types_allowed = True

    def __init__(self, **data):
        super().__init__(**data)
        if not self.controllers_manager:
            self.controllers_manager = ControllersManager()

    async def add_new_items(self, new_library_items: List[LibraryItem]):
        """
        Add new library items to the library system.

        Args:
            new_library_items (List[LibraryItem]): List of library items to add.
        """
        for new_library_item in new_library_items:
            if await self.controllers_manager.library_item_repo.item_exists(new_library_item.isbn):
                raise ItemAlreadyExistsError(new_library_item.isbn)
            new_library_item_document = item_pydantic_to_mongoengine(new_library_item)
            await self.controllers_manager.library_item_repo.add_library_item(new_library_item_document)
            logging.info(
                f"The library item {new_library_item.title} with ISBN {new_library_item.isbn} "
                f"was added to '{self.name}' library"
            )

    async def add_new_patrons(self, patrons_to_add: List[Patron]):
        """
        Add new patrons to the library system.

        Args:
            patrons_to_add (List[Patron]): List of patrons to add.
        """
        for patron in patrons_to_add:
            if await self.controllers_manager.patron_repo.patron_exists(patron.patron_id):
                raise PatronAlreadyExistsError(patron.patron_id)
            patron_document = patron_pydantic_to_mongoengine(patron)
            await self.controllers_manager.patron_repo.add_patron(patron_document)
            logging.info(f"The patron {patron.name} with ID {patron.patron_id} was added to the library")

    async def remove_patron(self, patron_id: str = Field(..., pattern=r'^\d{9}$')):
        """
        Remove patrons from the library system.

        Args:
            patron_id (str): ID of the patron to remove.
        """
        if not await self.controllers_manager.patron_repo.patron_exists(patron_id):
            raise PatronNotFoundError(patron_id)
        await self.controllers_manager.patron_repo.remove_patron({'patron_id': patron_id})
        logging.info(f"The patron {patron_id} was removed from the library")

    async def remove_item(self, library_item_isbn: str = Field(..., pattern=r'^\d{9}$')):
        """
        Remove an item from the library system by ISBN.

        Args:
            library_item_isbn (str): ISBN of the item to remove.
        """
        if not await self.controllers_manager.library_item_repo.item_exists(library_item_isbn):
            raise LibraryItemNotFoundError(item_isbn=library_item_isbn)
        if await self.controllers_manager.library_item_repo.is_item_borrowed(isbn=library_item_isbn):
            raise LibraryItemAlreadyBorrowedError(
                f"The library item with ISBN {library_item_isbn} is borrowed and cannot be removed")
        await self.controllers_manager.library_item_repo.remove_library_item({'isbn': library_item_isbn})
        logging.info(f"The item {library_item_isbn} was removed from the library")

    async def search_items(self, criteria: Dict[str, str]) -> List[LibraryItemDocument]:
        """
        Search for library items based on criteria.

        Args:
            criteria (Dict[str, str]): A dictionary with search criteria.

        Returns:
            List[LibraryItemDocument]: A list of matching library items.
        """
        return await self.controllers_manager.library_item_repo.search_items(criteria)
