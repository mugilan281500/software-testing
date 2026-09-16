from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import SecurityReport, AuditLog
from app.schemas import SecurityReportCreateSchema
from app.auth_utils import get_current_user
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["Reports & Audit"])

@router.get("", response_model=List[dict])
def list_reports(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    reports = db.query(SecurityReport).order_by(SecurityReport.id.desc()).all()
    return [
        {
            "id": r.id,
            "report_code": r.report_code,
            "title": r.title,
            "format": r.format,
            "risk_score": r.risk_score,
            "security_score": r.security_score,
            "created_by": r.created_by,
            "created_at": r.created_at
        } for r in reports
    ]

@router.post("/generate")
def generate_report(req: SecurityReportCreateSchema, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    report = ReportService.generate_report(db, title=req.title, report_format=req.format, created_by=current_user.username)
    return {"message": "Report generated successfully", "report_id": report.id, "file_name": report.file_name}

@router.get("/download/{report_id}")
def download_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(SecurityReport).filter(SecurityReport.id == report_id).first()
    if not report or not report.file_path:
        raise HTTPException(status_code=404, detail="Report file not found")
    return FileResponse(report.file_path, filename=report.file_name)

@router.get("/audit-logs")
def list_audit_logs(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return db.query(AuditLog).order_by(AuditLog.id.desc()).limit(100).all()
