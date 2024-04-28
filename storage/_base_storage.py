from abc import ABCMeta, abstractmethod
from uuid import UUID
from typing import List, TypeVar, Type, Optional, Tuple

from models import Entity


T = TypeVar("T", bound=Entity)


class BaseStorageABC(metaclass=ABCMeta):
    @abstractmethod
    def get(self, cls: Type[T], eid: UUID) -> T:
        pass

    @abstractmethod
    def try_get(self, cls: Type[T], eid: UUID) -> Tuple[bool, Optional[T]]:
        pass

    @abstractmethod
    def add_or_update(self, entity: T) -> UUID:
        pass

    @abstractmethod
    def update(self, entity: T) -> T:
        pass

    @abstractmethod
    def get_all(self, cls: Type[T]) -> List[T]:
        pass
