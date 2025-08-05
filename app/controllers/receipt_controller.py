#app/controllers/receipt_controller.py
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from app.database.connection_dependency import get_db
from app.services import receipt_service
from app.utils.auth_dependency import require_roles_dependency

router = APIRouter(prefix="/receipts", tags=["receipts"])

@router.post("/upload", status_code=201)
async def upload_receipt(
        file: UploadFile = File(...),
        user_id: int = Form(...),
        expense_type_id: int =  Form(...),
        amount: float = Form(...),
        description: str = Form(""),
        db: Session = Depends(get_db),
        current_user_role: str = Depends(require_roles_dependency(allowed_roles =["employee", "admin", "superadmin"]))
):
    try:
        result = await receipt_service.handle_receipt_upload(
            db =db,
            file =file,
            user_id=user_id,
            expense_type_id=expense_type_id,
            amount = amount,
            description=description
        )
        return JSONResponse(status_code=201, content={"message": "Receipt uploaded", "data": result })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))