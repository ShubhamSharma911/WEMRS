#app/services/cap_service.py

from decimal import Decimal
from sqlalchemy.orm import Session
from app.factories.capping_strategy_factory import get_capping_strategy

class CapService:
    def __init__(self, db: Session):
        self.db = db

    def get_cap_amount(self, emp_category_name: str, expense_type_id: int) -> Decimal:
        strategy = get_capping_strategy(emp_category_name, expense_type_id, self.db)
        return strategy.get_cap_amount(expense_type_id)
