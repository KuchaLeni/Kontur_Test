from clients import SpicesShopClient
from services import OrderService, SpicesService
from storage import Storage


class SpiceShopClientFactory:
    @staticmethod
    def create_client() -> SpicesShopClient:
        storage = Storage()
        return SpicesShopClient(OrderService(storage), SpicesService(storage))

    @classmethod
    def create(cls) -> SpicesShopClient:
        return cls.create_client()
