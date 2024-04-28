import copy
from typing import Type, List, Dict, Optional, Tuple
from uuid import UUID, uuid4

from models import Order, Spice
from ._base_storage import BaseStorageABC, T


class InMemoryStorage(BaseStorageABC):
    def __init__(self):
        self._data: Dict[str, Dict[UUID, T]] = {Order.__name__: {}, Spice.__name__: {}}

    def get(self, cls: Type[T], eid: UUID) -> T:
        """
        Retrieves entity of type [T] with specified
        :param cls: Model which entity should be founded
        :param eid: Id of entity to get
        :raises NameError: Unable to find entity with supplied eid
        :return: Copy of stored entity [T] with supplied eid.
        Modification of return value doesn't lead to change of stored data
        """
        found, entity = self.try_get(cls, eid)
        if not found:
            raise NameError(f"{cls.__name__} with {eid} doesn't exists")
        return entity  # type: ignore

    def try_get(self, cls: Type[T], eid: UUID) -> Tuple[bool, Optional[T]]:
        """
        Upsert entity of type [T] to store
        :param cls: Model which entity should be founded
        :param eid: Id of entity to get
        :return: 'True, <Instance>' when entity is found, 'False, None' otherwise
        """
        if cls.__name__ not in self._data.keys() or (entity := self._data[cls.__name__].get(eid, None)) is None:
            return False, None

        return True, copy.deepcopy(entity)

    def add_or_update(self, entity: T) -> UUID:
        """
        Upsert entity of type [T] to store
        Copy of supplied entity is stored,
        so modification of original object doesn't lead to modification of stored data
        :param entity: Instance of entity which would be inserted to storage
        :return: Id of upserted entity
        """
        if entity.eid is None:
            entity.eid = uuid4()

        self._data[entity.__class__.__name__][entity.eid] = copy.deepcopy(entity)

        return entity.eid

    def update(self, entity: T) -> T:
        """
        Updates entity of [T]
        :param entity: Entity to update
        :return: Updated entity
        """
        found, _ = self.try_get(entity.__class__, entity.eid) if entity.eid else (False, None)
        if not found:
            raise ValueError(f"{entity.__class__.__name__} with {entity.eid}" " which your try update, doesn't exists")

        eid = self.add_or_update(entity)
        return copy.deepcopy(self.get(entity.__class__, eid))

    def get_all(self, cls: Type[T]) -> List[T]:
        """
        Retrieves all stored entities of given type of <cls>
        :param cls: Entity class
        :return: List of entity
        """
        return list(self._data.get(cls.__name__, {}).values())
