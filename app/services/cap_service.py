# app/services/cap_service.py

from sqlalchemy.orm import Session
from decimal import Decimal
from app.factories.capping_strategy_factory import get_capping_strategy
from app.utils.logger import get_logger

logger = get_logger("CapService")
git add .
class CapService:
    def __init__(self, db: Session):
        self.db = db

    def get_cap(self, emp_category_name: str, expense_type_id: int) -> Decimal:
        logger.debug(f"Fetching cap for emp_category={emp_category_name}, expense_type_id={expense_type_id}")
        strategy = get_capping_strategy(emp_category_name, expense_type_id, self.db)
        cap_amount = strategy.get_cap_amount(expense_type_id)
        logger.info(f"Cap applied: ₹{cap_amount} for {emp_category_name} and type_id={expense_type_id}")
        return cap_amount
