#app/factories/capping_strategy_factory.py


from sqlalchemy.orm import Session
from app.strategies.capping_strategy import CappingStrategy
from app.strategies.db_capping_strategy import DBCappingStrategy

def get_capping_strategy(emp_category_name: str, expense_type_id: int, db: Session) -> CappingStrategy:
    return DBCappingStrategy(emp_category_name, expense_type_id, db)
