import re

from typing import List, Optional
from uuid import UUID, uuid4

from enums import UnitType
from exceptions import SpiceShopException
from models import Order, Spice
from ._base_service import BaseService


class OrderService(BaseService):
    def create_order(self, spice_id: UUID, quantity: int, customer_name: str) -> UUID:
        self.validate_order(spice_id, quantity, customer_name)

        self.update_available_spice(spice_id, quantity)
        return self.storage.add_or_update(
            Order(eid=uuid4(), quantity=quantity, customer_name=customer_name, spice_id=spice_id)
        )

    def get_order(self, order_id: UUID) -> Order:
        return self.storage.get(Order, order_id)

    def get_all_orders(self) -> List[Order]:
        return self.storage.get_all(Order)

    def update_available_spice(self, spice_id: UUID, quantity: int):
        spice = self.get_spice(spice_id)
        spice.available -= quantity
        self.storage.update(spice)

    def validate_order(self, spice_id: UUID, quantity: int, customer_name: str):
        spice = self.get_spice(spice_id)

        self.validate_quantity(quantity, spice.unit)
        self.validate_availability(quantity, spice.available)
        self.validate_customer_name(customer_name)

    def validate_quantity(self, quantity: int, unit: UnitType):
        match unit:
            case UnitType.GRAMS:
                self.validate_grams_quantity(quantity)
                return
            case UnitType.PIECES:
                self.validate_pieces_quantity(quantity)

    @staticmethod
    def validate_grams_quantity(quantity: int):
        if 1000 < quantity or quantity < 10:
            raise SpiceShopException("Quantity should be in range [10;1000]")

    @staticmethod
    def validate_pieces_quantity(quantity: int):
        if 10 < quantity or quantity < 1:
            raise SpiceShopException("Quantity should be in range [1;10]")

    @staticmethod
    def validate_availability(quantity: int, available: int):
        if quantity > available:
            raise SpiceShopException("Requested spice count exceeds remaining")

    @staticmethod
    def validate_customer_name(customer_name: str):
        if 20 < len(customer_name) or len(customer_name) < 3:
            raise SpiceShopException("Customer name should have length in range [3;20]")

        if not len(customer_name.strip()):
            raise SpiceShopException("Customer name should contain at least one non-whitespace character")

        if not bool(re.match(r"^[A-Za-zА-Яа-яЁёЙй ]+$", customer_name)):
            raise SpiceShopException("Customer name should contain only cyrillic or latin characters")

    def get_spice(self, spice_id: UUID) -> Spice:
        found, spice = self.storage.try_get(Spice, spice_id)
        if not found:
            raise SpiceShopException(f"Couldn't find Spice with id {spice_id}")
        return spice  # type: ignore
