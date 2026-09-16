from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import RiskRule, BankingRule, AuditLog
from app.schemas import RiskRuleUpdateSchema, BankingRuleUpdateSchema

router = APIRouter(prefix="/rules", tags=["Admin Rule Configuration Engine"])

@router.get("/security")
def get_security_risk_rules(db: Session = Depends(get_db)):
    rules = db.query(RiskRule).all()
    return rules

@router.put("/security")
def update_security_risk_rule(update_in: RiskRuleUpdateSchema, db: Session = Depends(get_db)):
    rule = db.query(RiskRule).filter(RiskRule.rule_key == update_in.rule_key).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Risk rule not found")

    if update_in.is_enabled is not None:
        rule.is_enabled = update_in.is_enabled
    if update_in.weight is not None:
        rule.weight = update_in.weight
    if update_in.params is not None:
        rule.params = update_in.params

    audit = AuditLog(
        user_email="admin@banksecure.io",
        action="RULE_CHANGED",
        resource=f"RISK_RULE-{rule.rule_key}",
        result="SUCCESS",
        details={"rule": rule.rule_key, "is_enabled": rule.is_enabled, "weight": rule.weight, "params": rule.params}
    )
    db.add(audit)
    db.commit()
    db.refresh(rule)

    return {"message": "Security risk rule updated successfully", "rule": rule}

@router.get("/banking")
def get_banking_business_rules(db: Session = Depends(get_db)):
    rules = db.query(BankingRule).all()
    return rules

@router.put("/banking")
def update_banking_business_rule(update_in: BankingRuleUpdateSchema, db: Session = Depends(get_db)):
    rule = db.query(BankingRule).filter(BankingRule.rule_code == update_in.rule_code).first()
    if not rule:
        raise HTTPException(status_code=404, detail="Banking rule not found")

    if update_in.is_enabled is not None:
        rule.is_enabled = update_in.is_enabled
    if update_in.threshold_value is not None:
        rule.threshold_value = update_in.threshold_value
    if update_in.action_on_fail is not None:
        rule.action_on_fail = update_in.action_on_fail
    if update_in.risk_weight is not None:
        rule.risk_weight = update_in.risk_weight

    audit = AuditLog(
        user_email="admin@banksecure.io",
        action="RULE_CHANGED",
        resource=f"BANKING_RULE-{rule.rule_code}",
        result="SUCCESS",
        details={"rule": rule.rule_code, "is_enabled": rule.is_enabled, "threshold": rule.threshold_value, "action": rule.action_on_fail}
    )
    db.add(audit)
    db.commit()
    db.refresh(rule)

    return {"message": "Banking business rule updated successfully", "rule": rule}
