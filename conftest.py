import pytest

from clients import SpicesShopClient
from services import OrderService, SpicesService
from storage import Storage


@pytest.fixture
def client():
    storage = Storage()
    return SpicesShopClient(OrderService(storage), SpicesService(storage))
