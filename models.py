from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from enums import UnitType


@dataclass
class Entity:
    """
    Attributes:
        eid (uuid4): Идентификатор сущности
    """

    eid: Optional[UUID]


@dataclass
class Order(Entity):
    """
    Attributes:
        spice_id (uuid4): Идентификатор заказанного продукта
        quantity (int): Количество товара для заказа
        customer_name (str): Полное имя покупателя
    """

    spice_id: UUID
    quantity: int
    customer_name: str


@dataclass
class Spice(Entity):
    """
    Attributes:
        unit (UnitType): Тип единиц
        name (str): Название
        available (int): Доступное для заказа количество
    """

    unit: UnitType
    name: str
    available: int
