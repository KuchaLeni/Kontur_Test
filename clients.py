from typing import Optional

from services import OrderService, SpicesService
from storage import BaseStorageABC, Storage


class SpicesShopClient:
    def __init__(self, orders: OrderService, spices: SpicesService):
        self._orders = orders
        self._spices = spices

    @property
    def orders(self):
        return self._orders

    @property
    def spices(self):
        return self._spices

    @classmethod
    def create(cls, storage: Optional[BaseStorageABC] = None):
        storage = storage if storage else Storage()

        return cls(OrderService(storage), SpicesService(storage))
