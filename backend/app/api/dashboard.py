from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import ApiTarget, TestRun, Finding, ThreatFlag
from app.schemas import DashboardSummarySchema
from app.auth_utils import get_current_user
from app.services.anomaly_detector import AnomalyDetector

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardSummarySchema)
def get_dashboard_summary(db: Session = Depends(get_db)):
    total_apis = db.query(ApiTarget).count()
    latest_run = db.query(TestRun).order_by(TestRun.id.desc()).first()

    tests_executed = latest_run.total_tests if latest_run else 0
    tests_passed = latest_run.passed if latest_run else 0
    tests_failed = latest_run.failed if latest_run else 0
    overall_risk_score = latest_run.overall_risk_score if latest_run else 22.5
    security_score = latest_run.security_score if latest_run else 77.5

    critical_findings = db.query(Finding).filter(Finding.severity == "CRITICAL", Finding.status == "OPEN").count()
    high_findings = db.query(Finding).filter(Finding.severity == "HIGH", Finding.status == "OPEN").count()
    active_flags = db.query(ThreatFlag).filter(ThreatFlag.status == "OPEN").count()

    risk_distribution = {
        "CRITICAL": db.query(Finding).filter(Finding.severity == "CRITICAL").count(),
        "HIGH": db.query(Finding).filter(Finding.severity == "HIGH").count(),
        "MEDIUM": db.query(Finding).filter(Finding.severity == "MEDIUM").count(),
        "LOW": db.query(Finding).filter(Finding.severity == "LOW").count(),
    }

    api_health = {
        "Authentication": 92.0,
        "Authorization": 74.0,
        "Validation": 88.0,
        "Business Logic": 69.0,
        "Headers": 95.0,
        "Rate Limiting": 61.0
    }

    anomalies = AnomalyDetector.get_active_anomalies(db)

    return {
        "total_apis": total_apis,
        "tests_executed": tests_executed,
        "tests_passed": tests_passed,
        "tests_failed": tests_failed,
        "critical_findings": critical_findings,
        "high_findings": high_findings,
        "active_flags": active_flags,
        "overall_risk_score": overall_risk_score,
        "security_score": security_score,
        "api_health": api_health,
        "risk_distribution": risk_distribution,
        "recent_alerts": anomalies
    }
