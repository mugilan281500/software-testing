from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Finding
from app.schemas import FindingResponseSchema, FindingUpdateSchema
from app.auth_utils import get_current_user

router = APIRouter(prefix="/findings", tags=["Security Findings"])

@router.get("", response_model=List[FindingResponseSchema])
def list_findings(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(Finding).order_by(Finding.id.desc()).all()

@router.get("/{finding_id}", response_model=FindingResponseSchema)
def get_finding(finding_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finding not found")
    return finding

@router.put("/{finding_id}", response_model=FindingResponseSchema)
def update_finding(finding_id: int, update_in: FindingUpdateSchema, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    finding = db.query(Finding).filter(Finding.id == finding_id).first()
    if not finding:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Finding not found")
    
    finding.status = update_in.status
    db.commit()
    db.refresh(finding)
    return finding
