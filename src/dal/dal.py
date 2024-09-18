from typing import TypeVar, Generic, Type, List, Optional, Dict

T = TypeVar("T")

class BaseRepository(Generic[T]):
    """
    A completely generic base repository for handling common CRUD operations.
    This class is backend-agnostic and can be extended for any specific database implementation (MongoDB, SQL, etc.).
    """

    def __init__(self, model: Type[T]):
        """
        Initialize the repository with a model class.
        The model class can represent any type (e.g., MongoDB document, SQL ORM model).

        :param model: The model class (e.g., MongoDB document or SQL ORM model).
        """
        self.model = model

    async def add(self, entity: T) -> None:
        """
        Adds a new entity to the storage backend.

        :param entity: The entity to be added.
        """
        await entity.insert()

    async def remove(self, query: Dict[str, Optional[str]]) -> None:
        """
        Removes an entity from the storage backend based on the provided query.

        :param query: The query dictionary to filter which entities should be removed.
        """
        await self.model.find(query).delete()

    async def update(self, entity: T) -> None:
        """
        Updates an existing entity in the storage backend.

        :param entity: The entity to be updated.
        """
        await entity.save()

    async def find_one(self, query: Dict[str, Optional[str]]) -> Optional[T]:
        """
        Finds a single entity based on the provided query.

        :param query: The query dictionary to filter the entities.
        :return: A single entity or None if not found.
        """
        return await self.model.find_one(query)

    async def find_all(self, query: Dict[str, Optional[str]]) -> List[T]:
        """
        Finds all entities that match the provided query.

        :param query: The query dictionary to filter the entities.
        :return: A list of entities matching the query.
        """
        return await self.model.find(query).to_list()

    async def exists(self, query: Dict[str, Optional[str]]) -> bool:
        """
        Checks whether any entity exists that matches the provided query.

        :param query: The query dictionary to filter the entities.
        :return: True if an entity exists, False otherwise.
        """
        return await self.model.find(query).count() > 0
