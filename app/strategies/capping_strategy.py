# app/strategies/capping_strategy.py

from abc import ABC, abstractmethod
from decimal import Decimal

class CappingStrategy(ABC):
    @abstractmethod
    def get_cap_amount(self, expense_type_id: int) -> Decimal:
        pass


class DefaultCappingStrategy(CappingStrategy):
    def get_cap_amount(self, expense_type_id: int) -> Decimal:
        # Fallback cap if no record in DB
        return Decimal("1000.00")
