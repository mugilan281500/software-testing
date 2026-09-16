from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas import SandboxToggleSchema, SandboxToggleUpdateSchema, MockTransferSchema
from app.services.mock_bank_service import MockBankService
from app.services.transaction_monitor import RealTimeTransactionMonitorEngine
from app.models import MockAccount, MockBeneficiary, MockTransaction

router = APIRouter(prefix="/mock-bank", tags=["Mock Banking Sandbox"])

@router.get("/sandbox/toggles", response_model=List[SandboxToggleSchema])
def get_sandbox_toggles(db: Session = Depends(get_db)):
    return MockBankService.get_toggles(db)

@router.put("/sandbox/toggles")
def update_sandbox_toggle(update_in: SandboxToggleUpdateSchema, db: Session = Depends(get_db)):
    toggle = MockBankService.set_toggle(db, update_in.key, update_in.is_enabled)
    if not toggle:
        raise HTTPException(status_code=404, detail="Toggle key not found")
    return {"message": "Toggle updated successfully", "toggle": toggle}

@router.get("/accounts")
def list_mock_accounts(db: Session = Depends(get_db)):
    return db.query(MockAccount).all()

@router.get("/beneficiaries/{account_number}")
def list_beneficiaries(account_number: str, db: Session = Depends(get_db)):
    return db.query(MockBeneficiary).filter(MockBeneficiary.account_number == account_number).all()

@router.get("/transactions")
def list_mock_transactions(db: Session = Depends(get_db)):
    return db.query(MockTransaction).order_by(MockTransaction.id.desc()).all()

@router.post("/transfer")
def execute_transfer(transfer_in: MockTransferSchema, db: Session = Depends(get_db)):
    # Every manual transaction automatically passes through the real-time security monitoring engine!
    monitoring_result = RealTimeTransactionMonitorEngine.monitor_transaction(
        db,
        sender_acc_num=transfer_in.sender_account,
        receiver_acc_num=transfer_in.receiver_account,
        amount=transfer_in.amount,
        currency=transfer_in.currency or "INR",
        device_id=transfer_in.device_id or "DEVICE-001",
        ip_address=transfer_in.ip_address or "192.168.1.50"
    )

    if not monitoring_result["success"]:
        raise HTTPException(
            status_code=400,
            detail={
                "message": monitoring_result["message"],
                "decision": monitoring_result["decision"],
                "risk_score": monitoring_result["risk_score"],
                "risk_level": monitoring_result["risk_level"],
                "indicators": monitoring_result["indicators"]
            }
        )

    return monitoring_result

