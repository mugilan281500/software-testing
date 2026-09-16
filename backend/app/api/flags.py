from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import ThreatFlag
from app.schemas import ThreatFlagResponseSchema, ThreatFlagUpdateSchema
from app.auth_utils import get_current_user

router = APIRouter(prefix="/flags", tags=["Threat Flags"])

@router.get("", response_model=List[ThreatFlagResponseSchema])
def list_flags(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(ThreatFlag).order_by(ThreatFlag.id.desc()).all()

@router.get("/{flag_id}", response_model=ThreatFlagResponseSchema)
def get_flag(flag_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    flag = db.query(ThreatFlag).filter(ThreatFlag.id == flag_id).first()
    if not flag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Threat flag not found")
    return flag

@router.put("/{flag_id}", response_model=ThreatFlagResponseSchema)
def update_flag(flag_id: int, update_in: ThreatFlagUpdateSchema, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    flag = db.query(ThreatFlag).filter(ThreatFlag.id == flag_id).first()
    if not flag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Threat flag not found")
    
    flag.status = update_in.status
    if update_in.analyst_notes:
        flag.analyst_notes = update_in.analyst_notes
    db.commit()
    db.refresh(flag)
    return flag
