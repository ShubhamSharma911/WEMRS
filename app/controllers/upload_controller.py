from fastapi import APIRouter, UploadFile, File, Request, HTTPException, status, Depends
from app.services.upload_service import UploadService
from app.utils.auth_dependency import require_roles_dependency
from sqlalchemy.orm import Session
from app.database.connection_dependency import get_db

router = APIRouter(prefix="/upload", tags=["Expense Upload"])

@router.post("/", dependencies=[Depends(require_roles_dependency(["EMPLOYEE"]))])
async def upload_expense(
    request: Request,
    file: UploadFile = File(...),
    description: str = None,
    db: Session = Depends(get_db)
):
    try:
        user_id = request.state.current_user_id
        upload_service = UploadService(db)
        saved_file_name = await upload_service.handle_upload(file, user_id=user_id, description=description)
        return {"filename": saved_file_name}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
