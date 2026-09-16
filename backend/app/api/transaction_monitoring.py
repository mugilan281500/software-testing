from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import MockTransaction, TransactionRiskScore, TransactionSecurityEvent, BehaviorProfile

router = APIRouter(prefix="/monitoring", tags=["Real-Time Security Monitoring Engine"])

@router.get("/live-feed")
def get_live_monitoring_feed(db: Session = Depends(get_db)):
    txs = db.query(MockTransaction).order_by(MockTransaction.id.desc()).limit(50).all()

    total_count = len(txs)
    normal_count = sum(1 for t in txs if t.risk_level == "LOW")
    monitored_count = sum(1 for t in txs if t.risk_level == "MEDIUM")
    flagged_count = sum(1 for t in txs if t.risk_level == "HIGH")
    critical_count = sum(1 for t in txs if t.risk_level == "CRITICAL")

    feed = [
        {
            "id": t.id,
            "transaction_id": t.transaction_id,
            "sender": t.sender_account,
            "receiver": t.receiver_account,
            "amount": t.amount,
            "currency": t.currency,
            "risk_score": t.risk_score,
            "risk_level": t.risk_level,
            "flags": t.flags_count,
            "decision": t.decision,
            "status": t.status,
            "device_id": t.device_id,
            "ip_address": t.ip_address,
            "timestamp": t.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for t in txs
    ]

    return {
        "summary": {
            "total": total_count,
            "normal": normal_count,
            "monitored": monitored_count,
            "flagged": flagged_count,
            "critical": critical_count
        },
        "transactions": feed
    }

@router.get("/transactions/{transaction_id}/scorecard")
def get_transaction_explainable_scorecard(transaction_id: str, db: Session = Depends(get_db)):
    tx = db.query(MockTransaction).filter(MockTransaction.transaction_id == transaction_id).first()
    if not tx:
        raise HTTPException(status_code=404, detail="Transaction not found")

    scorecard = db.query(TransactionRiskScore).filter(TransactionRiskScore.transaction_id == transaction_id).first()
    events = db.query(TransactionSecurityEvent).filter(TransactionSecurityEvent.transaction_id == transaction_id).all()

    return {
        "transaction_id": tx.transaction_id,
        "sender": tx.sender_account,
        "receiver": tx.receiver_account,
        "amount": tx.amount,
        "currency": tx.currency,
        "risk_score": tx.risk_score,
        "risk_level": tx.risk_level,
        "decision": tx.decision,
        "device_id": tx.device_id,
        "ip_address": tx.ip_address,
        "timestamp": tx.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "scorecard": {
            "auth_score": scorecard.auth_score if scorecard else 100.0,
            "authz_score": scorecard.authz_score if scorecard else 100.0,
            "validation_score": scorecard.validation_score if scorecard else 100.0,
            "business_rules_score": scorecard.business_rules_score if scorecard else 100.0,
            "behavior_score": scorecard.behavior_score if scorecard else 100.0,
            "api_security_score": scorecard.api_security_score if scorecard else 100.0,
            "overall_score": scorecard.overall_score if scorecard else tx.risk_score
        },
        "explainable_risk_factors": scorecard.factors_json if scorecard else [],
        "security_events": [
            {
                "code": e.indicator_code,
                "name": e.indicator_name,
                "severity": e.severity,
                "impact": e.score_impact,
                "explanation": e.explanation
            }
            for e in events
        ]
    }

@router.get("/timeline")
def get_transaction_risk_timeline(db: Session = Depends(get_db)):
    txs = db.query(MockTransaction).order_by(MockTransaction.id.asc()).limit(30).all()
    timeline = [
        {
            "tx_id": t.transaction_id,
            "timestamp": t.timestamp.strftime("%H:%M:%S"),
            "risk_score": t.risk_score,
            "risk_level": t.risk_level,
            "amount": t.amount,
            "flags": t.flags_count,
            "decision": t.decision
        }
        for t in txs
    ]
    return timeline

@router.get("/baseline/{account_number}")
def get_user_baseline_profile(account_number: str, db: Session = Depends(get_db)):
    profile = db.query(BehaviorProfile).filter(BehaviorProfile.account_number == account_number).first()
    if not profile:
        return {
            "account_number": account_number,
            "normal_range": "₹1,000 – ₹25,000",
            "avg_amount": 5000.0,
            "max_normal": 50000.0,
            "normal_frequency": "1–5 txns/day",
            "normal_hours": "08:00–22:00",
            "known_devices": ["DEVICE-001"],
            "known_ips": ["192.168.1.50"]
        }
    return {
        "account_number": profile.account_number,
        "username": profile.username,
        "avg_amount": profile.avg_amount,
        "normal_min_amount": profile.normal_min_amount,
        "normal_max_amount": profile.normal_max_amount,
        "max_normal_transaction": profile.max_normal_transaction,
        "normal_frequency": f"{int(profile.avg_daily_frequency)} txns/day",
        "normal_hours": f"{profile.normal_start_hour:02d}:00–{profile.normal_end_hour:02d}:00",
        "known_devices": profile.known_devices,
        "known_ips": profile.known_ips
    }
