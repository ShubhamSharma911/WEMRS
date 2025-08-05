#app/repositories/cap_repository.py


from sqlalchemy.orm import Session
from sqlalchemy import text
from decimal import Decimal

def get_cap_amount(emp_category_name: str, expense_type_id: int, db: Session) -> Decimal | None:
    query = text("""
        SELECT cap_amount FROM expense_caps
        WHERE emp_category_id = (
            SELECT id FROM emp_categories WHERE name = :category_name
        )
        AND expense_type_id = :expense_type_id
    """)

    result = db.execute(query, {
        "category_name": emp_category_name,
        "expense_type_id": expense_type_id
    }).fetchone()

    return Decimal(result[0]) if result else None
