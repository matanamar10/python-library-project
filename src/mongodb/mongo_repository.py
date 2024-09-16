from typing import List, Optional
from src.mongodb.mongodb_models.library_item_model import LibraryItemDocument
from typing import Dict
from src.mongodb.mongodb_models.patron_model import PatronDocument
from src.mongodb.mongodb_models.bills_model import BillDocument


class MongoLibraryItemRepository:
    """
    A repository class for managing LibraryItemDocument operations in MongoDB.
    """

    async def update_item_status(self, isbn: str, is_borrowed: bool) -> None:
        """
        Updates the borrowed status of a library item by ISBN.

        :param isbn: The ISBN of the library item.
        :param is_borrowed: Boolean indicating whether the item is borrowed.
        """
        item = await LibraryItemDocument.find_one(LibraryItemDocument.isbn == isbn)
        if item:
            item.is_borrowed = is_borrowed
            await item.save()

    async def add_library_item(self, document: LibraryItemDocument) -> None:
        """
        Adds a new LibraryItemDocument into the MongoDB collection.

        :param document: The LibraryItemDocument to be added.
        """
        await document.insert()

    async def remove_library_item(self, query: Dict[str, str]) -> None:
        """
        Removes a LibraryItemDocument from the MongoDB collection based on the provided query.

        :param query: Dictionary specifying the query to match documents for removal.
        """
        await LibraryItemDocument.find(query).delete()

    async def item_exists(self, isbn: str) -> bool:
        """
        Checks whether a library item with the given ISBN exists.

        :param isbn: The ISBN of the library item.
        :return: True if the item exists, False otherwise.
        """
        return await LibraryItemDocument.find(LibraryItemDocument.isbn == isbn).count() > 0

    async def is_item_borrowed(self, isbn: str) -> bool:
        """
        Checks whether a library item is borrowed by its ISBN.

        :param isbn: The ISBN of the library item.
        :return: True if the item is borrowed, False otherwise.
        """
        item = await LibraryItemDocument.find_one(LibraryItemDocument.isbn == isbn)
        return item.is_borrowed if item else False

    async def search_items(self, query: Dict[str, Optional[str]]) -> List[LibraryItemDocument]:
        """
        Searches for library items based on the provided query.

        :param query: Dictionary specifying the search criteria.
        :return: A list of LibraryItemDocuments matching the query.
        """
        return await LibraryItemDocument.find(query).to_list()


class MongoPatronRepository:
    """
    A repository class for managing PatronDocument operations in MongoDB.
    """

    async def return_item(self, patron_id: str, isbn: str) -> None:
        """
        Removes an item from a patron's borrowed list by ISBN.

        :param patron_id: The ID of the patron.
        :param isbn: The ISBN of the item to be returned.
        """
        patron = await PatronDocument.find_one(PatronDocument.id == patron_id)
        if patron:
            patron.items.pop(isbn, None)
            await patron.save()

    async def borrow_item(self, patron_id: str, isbn: str, borrow_date) -> None:
        """
        Adds an item to a patron's borrowed list by ISBN.

        :param patron_id: The ID of the patron.
        :param isbn: The ISBN of the item to be borrowed.
        :param borrow_date: The date when the item was borrowed.
        """
        patron = await PatronDocument.find_one(PatronDocument.id == patron_id)
        if patron:
            patron.items[isbn] = borrow_date
            await patron.save()

    class MongoPatronRepository:
        """
        A repository class for managing PatronDocument operations in MongoDB.
        """

        async def add_patron(self, document: PatronDocument) -> None:
            """
            Adds a new PatronDocument into the MongoDB collection.

            :param document: The PatronDocument to be added.
            """
            await document.insert()

        async def remove_patron(self, query: Dict) -> None:
            """
            Removes a PatronDocument from the MongoDB collection based on the provided query.

            :param query: Dictionary specifying the query to match documents for removal.
            """
            await PatronDocument.find(query).delete()

    async def patron_exists(self, patron_id: str) -> bool:
        """
        Checks whether a patron with the given ID exists.

        :param patron_id: The ID of the patron.
        :return: True if the patron exists, False otherwise.
        """
        return await PatronDocument.find(PatronDocument.id == patron_id).count() > 0


class MongoBillRepository:
    """
    A repository class for managing BillDocument operations in MongoDB.
    """

    async def insert_bill(self, patron_id: str, amount: float) -> None:
        """
        Inserts a new bill for a patron.

        :param patron_id: The ID of the patron to whom the bill belongs.
        :param amount: The amount of the bill.
        """
        bill = BillDocument(patron_id=patron_id, patron_bill_sum=amount)
        await bill.insert()

    async def update_bill(self, patron_id: str, amount: float) -> None:
        """
        Updates the bill amount for a patron.

        :param patron_id: The ID of the patron to whom the bill belongs.
        :param amount: The updated bill amount.
        """
        bill = await BillDocument.find_one(BillDocument.patron_id == patron_id)
        if bill:
            bill.patron_bill_sum = amount
            await bill.save()

    async def delete_bill(self, patron_id: str) -> None:
        """
        Deletes a bill for a specific patron.

        :param patron_id: The ID of the patron whose bill is to be deleted.
        """
        await BillDocument.find(BillDocument.patron_id == patron_id).delete()
