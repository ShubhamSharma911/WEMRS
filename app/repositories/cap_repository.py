# app/repositories/cap_repository.py

from sqlalchemy.orm import Session
from sqlalchemy import text
from decimal import Decimal
from app.utils.logger import get_logger

logger = get_logger("CapRepository")

def get_cap_amount(emp_category_name: str, expense_type_id: int, db: Session) -> Decimal | None:
    """
    Fetch cap amount for a given employee category and expense type.
    """
    try:
        query = text("""
            SELECT ec.cap_amount
            FROM expense_caps ec
            JOIN emp_categories cat ON ec.emp_category_id = cat.id
            WHERE cat.name = :category_name AND ec.expense_type_id = :expense_type_id
        """)

        result = db.execute(query, {
            "category_name": emp_category_name,
            "expense_type_id": expense_type_id
        }).fetchone()

        if result:
            logger.debug(f"Cap found: category={emp_category_name}, type_id={expense_type_id}, cap={result.cap_amount}")
            return Decimal(result.cap_amount)

        logger.warning(f"No cap found for category={emp_category_name}, type_id={expense_type_id}")
        return None

    except Exception as e:
        logger.error(f"Error fetching cap for category={emp_category_name}, type_id={expense_type_id}: {e}", exc_info=True)
        return None
