from storage import BaseStorageABC


class BaseService:
    def __init__(self, storage: BaseStorageABC):
        self.__storage = storage

    @property
    def storage(self) -> BaseStorageABC:
        return self.__storage
