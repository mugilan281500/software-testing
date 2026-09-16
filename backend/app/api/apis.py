from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import ApiTarget
from app.schemas import ApiTargetCreateSchema, ApiTargetResponseSchema
from app.auth_utils import get_current_user

router = APIRouter(prefix="/apis", tags=["API Inventory"])

@router.get("", response_model=List[ApiTargetResponseSchema])
def list_apis(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(ApiTarget).all()

@router.post("", response_model=ApiTargetResponseSchema)
def create_api(api_in: ApiTargetCreateSchema, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    api_obj = ApiTarget(**api_in.model_dump())
    db.add(api_obj)
    db.commit()
    db.refresh(api_obj)
    return api_obj

@router.get("/{api_id}", response_model=ApiTargetResponseSchema)
def get_api(api_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    target = db.query(ApiTarget).filter(ApiTarget.id == api_id).first()
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API target not found")
    return target

@router.put("/{api_id}", response_model=ApiTargetResponseSchema)
def update_api(api_id: int, api_in: ApiTargetCreateSchema, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    target = db.query(ApiTarget).filter(ApiTarget.id == api_id).first()
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API target not found")
    
    for key, value in api_in.model_dump().items():
        setattr(target, key, value)
        
    db.commit()
    db.refresh(target)
    return target

@router.delete("/{api_id}")
def delete_api(api_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    target = db.query(ApiTarget).filter(ApiTarget.id == api_id).first()
    if not target:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="API target not found")
    db.delete(target)
    db.commit()
    return {"message": "API target deleted successfully"}
