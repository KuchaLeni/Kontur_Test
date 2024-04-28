from typing import List, Optional
from uuid import UUID

from enums import UnitType
from models import Spice
from ._base_service import BaseService


class SpicesService(BaseService):
    def add_spice(self, name: str, unit: UnitType, remaining: int):
        if remaining < 0:
            raise ValueError("Remaining should be non-negative")

        return self.storage.add_or_update(Spice(eid=None, available=remaining, name=name, unit=unit))

    def inc_remaining(self, spice_id: UUID, value: int):
        spice = self.get_spice(spice_id)
        spice.available += value
        return self.storage.update(spice)

    def get_spice(self, spice_id: UUID) -> Spice:
        return self.storage.get(Spice, spice_id)

    def get_spices(self) -> List[Spice]:
        return self.storage.get_all(Spice)
