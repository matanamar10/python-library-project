from src.dal.dal import BaseRepository
from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument


class MongoLibraryItemRepository(BaseRepository[LibraryItemDocument]):
    """
    A MongoDB-specific repository for managing LibraryItemDocument operations.
    """

    def __init__(self):
        super().__init__(LibraryItemDocument)

    async def update_item_status(self, isbn: str, is_borrowed: bool) -> None:
        """
        Updates the borrowed status of a library item by ISBN.

        :param isbn: The ISBN of the library item.
        :param is_borrowed: Boolean indicating whether the item is borrowed.
        """
        item = await self.find_one({"isbn": isbn})
        if item:
            item.is_borrowed = is_borrowed
            await self.update(item)

    async def is_item_borrowed(self, isbn: str) -> bool:
        """
        Checks whether a library item is borrowed by its ISBN.

        :param isbn: The ISBN of the library item.
        :return: True if the item is borrowed, False otherwise.
        """
        item = await self.find_one({"isbn": isbn})
        return item.is_borrowed if item else False

from src.mongodb.mongodb_models.patron_model import PatronDocument

class MongoPatronRepository(BaseRepository[PatronDocument]):
    """
    A MongoDB-specific repository for managing PatronDocument operations.
    Includes domain-specific operations like borrowing and returning items.
    """

    def __init__(self):
        super().__init__(PatronDocument)

    async def borrow_item(self, patron_id: str, isbn: str, borrow_date: str) -> None:
        """
        Adds an item to a patron's borrowed list by ISBN.

        :param patron_id: The ID of the patron.
        :param isbn: The ISBN of the item to be borrowed.
        :param borrow_date: The date when the item was borrowed.
        """
        patron = await self.find_one({"id": patron_id})
        if patron:
            patron.items[isbn] = borrow_date
            await self.update(patron)

    async def return_item(self, patron_id: str, isbn: str) -> None:
        """
        Removes an item from a patron's borrowed list by ISBN.

        :param patron_id: The ID of the patron.
        :param isbn: The ISBN of the item to be returned.
        """
        patron = await self.find_one({"id": patron_id})
        if patron:
            patron.items.pop(isbn, None)
            await self.update(patron)

    async def patron_exists(self, patron_id: str) -> bool:
        """
        Checks whether a patron with the given ID exists.

        :param patron_id: The ID of the patron.
        :return: True if the patron exists, False otherwise.
        """
        return await self.exists({"id": patron_id})

from src.mongodb.mongodb_models.bills_model import BillDocument

class MongoBillRepository(BaseRepository[BillDocument]):
    """
    A MongoDB-specific repository for managing BillDocument operations.
    """

    def __init__(self):
        super().__init__(BillDocument)

    async def insert_bill(self, patron_id: str, amount: float) -> None:
        """
        Inserts a new bill for a patron.

        :param patron_id: The ID of the patron to whom the bill belongs.
        :param amount: The amount of the bill.
        """
        bill = BillDocument(patron_id=patron_id, patron_bill_sum=amount)
        await self.add(bill)

    async def update_bill(self, patron_id: str, amount: float) -> None:
        """
        Updates the bill amount for a patron.

        :param patron_id: The ID of the patron to whom the bill belongs.
        :param amount: The updated bill amount.
        """
        bill = await self.find_one({"patron_id": patron_id})
        if bill:
            bill.patron_bill_sum = amount
            await self.update(bill)

    async def delete_bill(self, patron_id: str) -> None:
        """
        Deletes a bill for a specific patron.

        :param patron_id: The ID of the patron whose bill is to be deleted.
        """
        await self.remove({"patron_id": patron_id})
