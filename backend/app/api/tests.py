from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models import TestCase, TestRun, TestResult
from app.schemas import (
    TestCaseResponseSchema, TestRunResponseSchema, TestRunRequestSchema,
    SelectedTestsRunRequestSchema, OpenApiImportSchema
)
from app.services.test_orchestrator import TestOrchestratorService
from app.services.api_change_detector import ApiChangeDetectorService

router = APIRouter(prefix="/tests", tags=["Testing Engine & Orchestration"])

@router.get("/cases")
def list_test_cases(db: Session = Depends(get_db)):
    return db.query(TestCase).all()

@router.get("/queue")
def get_adaptive_test_queue(db: Session = Depends(get_db)):
    return TestOrchestratorService.get_adaptive_test_queue(db)

@router.post("/run-full")
def run_full_automated_test(db: Session = Depends(get_db)):
    return TestOrchestratorService.execute_test_suite(db, selected_modules=None, trigger_source="MANUAL_FULL_SUITE")

@router.post("/run-selected")
def run_selected_module_tests(req: SelectedTestsRunRequestSchema, db: Session = Depends(get_db)):
    if not req.modules:
        raise HTTPException(status_code=400, detail="Please select at least one test module")
    return TestOrchestratorService.execute_test_suite(db, selected_modules=req.modules, trigger_source="MANUAL_SELECTED")

@router.post("/openapi-import")
def import_and_detect_api_changes(req: OpenApiImportSchema, db: Session = Depends(get_db)):
    return ApiChangeDetectorService.process_openapi_import(
        db, title=req.title, version=req.version, endpoints=req.endpoints_json
    )

@router.get("/runs")
def list_test_runs(db: Session = Depends(get_db)):
    return db.query(TestRun).order_by(TestRun.id.desc()).all()

@router.get("/runs/{run_id}")
def get_test_run(run_id: int, db: Session = Depends(get_db)):
    run = db.query(TestRun).filter(TestRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Test run not found")
    results = db.query(TestResult).filter(TestResult.test_run_id == run_id).all()
    return {
        "id": run.id,
        "run_number": run.run_number,
        "execution_type": run.execution_type,
        "total_tests": run.total_tests,
        "passed": run.passed,
        "failed": run.failed,
        "critical_count": run.critical_count,
        "high_count": run.high_count,
        "overall_risk_score": run.overall_risk_score,
        "security_score": run.security_score,
        "duration_ms": run.duration_ms,
        "status": run.status,
        "executed_by": run.executed_by,
        "started_at": run.started_at,
        "completed_at": run.completed_at,
        "results": [
            {
                "id": r.id,
                "test_case_id": r.test_case_id,
                "test_name": r.test_name,
                "category": r.category,
                "api_endpoint": r.api_endpoint,
                "status": r.status,
                "severity": r.severity,
                "risk_score": r.risk_score,
                "actual_status": r.actual_status,
                "response_time_ms": r.response_time_ms,
                "evidence": r.evidence,
                "recommendation": r.recommendation
            }
            for r in results
        ]
    }

