# app/factories/capping_strategy_factory.py

from sqlalchemy.orm import Session
from app.repositories.cap_repository import get_cap_amount
from app.strategies.capping_strategy import CappingStrategy, DefaultCappingStrategy
from decimal import Decimal

class DBCappingStrategy(CappingStrategy):
    def __init__(self, emp_category_name: str, expense_type_id: int, db: Session):
        self.emp_category_name = emp_category_name
        self.expense_type_id = expense_type_id
        self.db = db

    def get_cap_amount(self, expense_type_id: int) -> Decimal:
        cap = get_cap_amount(self.emp_category_name, expense_type_id, self.db)
        return cap if cap is not None else Decimal("1000.00")


def get_capping_strategy(emp_category_name: str, expense_type_id: int, db: Session) -> CappingStrategy:
    return DBCappingStrategy(emp_category_name, expense_type_id, db)
