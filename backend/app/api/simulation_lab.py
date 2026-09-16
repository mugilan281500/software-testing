from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import datetime
from app.database import get_db
from app.schemas import ScenarioRunRequestSchema
from app.services.transaction_monitor import RealTimeTransactionMonitorEngine
from app.models import LoginAttempt

router = APIRouter(prefix="/simulation", tags=["Transaction Security Lab"])

@router.get("/scenarios")
def get_available_scenarios():
    return [
        {"key": "NORMAL", "name": "Normal Transaction", "description": "Standard transfer within historical average amount and known device", "expected_risk": "LOW (0-29)"},
        {"key": "HIGH_AMOUNT", "name": "Unusual High Amount", "description": "Transfer ₹85,000 exceeding historical user baseline", "expected_risk": "HIGH / CRITICAL"},
        {"key": "RAPID_TXNS", "name": "Rapid Sequential Transfers", "description": "Execute 4 rapid transactions within 60 seconds", "expected_risk": "HIGH"},
        {"key": "NEW_DEVICE", "name": "Unrecognized New Device", "description": "Transfer originating from unknown Device ID (DEVICE-999)", "expected_risk": "MEDIUM / HIGH"},
        {"key": "IP_CHANGE", "name": "Synthetic IP Metadata Shift", "description": "Transfer originating from IP 203.0.113.195 (Unrecognized Geo)", "expected_risk": "MEDIUM"},
        {"key": "FAILED_LOGIN_TRANSFER", "name": "Failed Login + Immediate Transfer", "description": "Simulate 3 failed password attempts followed immediately by a transfer", "expected_risk": "HIGH / CRITICAL"},
        {"key": "DUPLICATE_TXN", "name": "Duplicate Transaction", "description": "Execute identical transfer amount to same recipient twice in 30 seconds", "expected_risk": "MEDIUM"},
        {"key": "LIMIT_VIOLATION", "name": "Daily Transfer Limit Violation", "description": "Transfer ₹120,000 exceeding daily account limit (₹100,000)", "expected_risk": "CRITICAL"},
        {"key": "COMBINED_SUSPICIOUS", "name": "Combined Multi-Factor Attack Scenario", "description": "Failed Login + New Device + IP Change + ₹95,000 High Amount", "expected_risk": "CRITICAL (80-100)"}
    ]

@router.post("/run-scenario")
def run_synthetic_scenario(payload: ScenarioRunRequestSchema, db: Session = Depends(get_db)):
    key = payload.scenario_key.upper()
    sender = payload.sender_account or "ACC-1001"
    receiver = payload.receiver_account or "ACC-1002"

    if key == "NORMAL":
        res = RealTimeTransactionMonitorEngine.monitor_transaction(
            db, sender, receiver, amount=3500.0, device_id="DEVICE-001", ip_address="192.168.1.50"
        )
    elif key == "HIGH_AMOUNT":
        res = RealTimeTransactionMonitorEngine.monitor_transaction(
            db, sender, receiver, amount=85000.0, device_id="DEVICE-001", ip_address="192.168.1.50"
        )
    elif key == "RAPID_TXNS":
        # Execute 3 rapid txns first, then monitor 4th
        for i in range(3):
            RealTimeTransactionMonitorEngine.monitor_transaction(
                db, sender, receiver, amount=2000.0 + (i * 500), device_id="DEVICE-001", ip_address="192.168.1.50"
            )
        res = RealTimeTransactionMonitorEngine.monitor_transaction(
            db, sender, receiver, amount=60000.0, device_id="DEVICE-001", ip_address="192.168.1.50"
        )
    elif key == "NEW_DEVICE":
        res = RealTimeTransactionMonitorEngine.monitor_transaction(
            db, sender, receiver, amount=12000.0, device_id="DEVICE-UNKNOWN-999", ip_address="192.168.1.50"
        )
    elif key == "IP_CHANGE":
        res = RealTimeTransactionMonitorEngine.monitor_transaction(
            db, sender, receiver, amount=15000.0, device_id="DEVICE-001", ip_address="203.0.113.195"
        )
    elif key == "FAILED_LOGIN_TRANSFER":
        # Inject failed logins
        username = f"user_{sender[-4:]}"
        for _ in range(3):
            db.add(LoginAttempt(username=username, ip_address="203.0.113.195", status="FAILED", reason="Invalid password"))
        db.commit()

        res = RealTimeTransactionMonitorEngine.monitor_transaction(
            db, sender, receiver, amount=45000.0, device_id="DEVICE-001", ip_address="203.0.113.195"
        )
    elif key == "DUPLICATE_TXN":
        # Execute initial transfer
        RealTimeTransactionMonitorEngine.monitor_transaction(
            db, sender, receiver, amount=25000.0, device_id="DEVICE-001", ip_address="192.168.1.50"
        )
        res = RealTimeTransactionMonitorEngine.monitor_transaction(
            db, sender, receiver, amount=25000.0, device_id="DEVICE-001", ip_address="192.168.1.50"
        )
    elif key == "LIMIT_VIOLATION":
        res = RealTimeTransactionMonitorEngine.monitor_transaction(
            db, sender, receiver, amount=120000.0, device_id="DEVICE-001", ip_address="192.168.1.50"
        )
    elif key == "COMBINED_SUSPICIOUS":
        username = f"user_{sender[-4:]}"
        for _ in range(4):
            db.add(LoginAttempt(username=username, ip_address="198.51.100.88", status="FAILED", reason="Brute force login"))
        db.commit()

        # Previous rapid txns
        RealTimeTransactionMonitorEngine.monitor_transaction(
            db, sender, receiver, amount=10000.0, device_id="DEVICE-ATTACKER-999", ip_address="198.51.100.88"
        )

        res = RealTimeTransactionMonitorEngine.monitor_transaction(
            db, sender, receiver, amount=95000.0, device_id="DEVICE-ATTACKER-999", ip_address="198.51.100.88"
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid simulation scenario key")

    return {
        "scenario": key,
        "execution_status": "SUCCESS",
        "result": res
    }
