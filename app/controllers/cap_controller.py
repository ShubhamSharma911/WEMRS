#app/controllers/cap_controller.py

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session
from app.services.cap_service import CapService
from app.database.connection_dependency import get_db

router = APIRouter(prefix="/caps", tags=["Capping"])

@router.get("/{emp_category_name}/{expense_type_id}")
def get_cap(emp_category_name: str, expense_type_id: int, db: Session = Depends(get_db)):
    service = CapService(db)
    cap = service.get_cap_amount(emp_category_name, expense_type_id)
    return {"cap_amount": float(cap)}
