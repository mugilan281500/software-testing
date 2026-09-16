from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth_utils import get_current_user
from app.services.smart_analytics import SmartAnalytics

router = APIRouter(prefix="/analytics", tags=["Smart Quality & Analytics"])

@router.get("/quality-gate")
def get_quality_gate_metrics(db: Session = Depends(get_db)):
    return SmartAnalytics.get_release_readiness(db)

@router.post("/auto-generate-tests/{api_id}")
def auto_generate_tests(api_id: int, db: Session = Depends(get_db)):
    generated = SmartAnalytics.auto_generate_tests_for_api(db, api_id)
    return {
        "message": f"Successfully auto-generated {len(generated)} security test vectors",
        "generated_count": len(generated),
        "test_ids": [g.test_id for g in generated]
    }
