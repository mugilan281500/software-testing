import uuid
from sqlalchemy.orm import Session
from app.models import MockAccount, MockTransaction, MockSandboxToggle

class MockBankService:
    @staticmethod
    def get_toggles(db: Session):
        return db.query(MockSandboxToggle).all()

    @staticmethod
    def set_toggle(db: Session, key: str, is_enabled: bool):
        toggle = db.query(MockSandboxToggle).filter(MockSandboxToggle.key == key).first()
        if toggle:
            toggle.is_enabled = is_enabled
            db.commit()
            db.refresh(toggle)
        return toggle

    @staticmethod
    def is_vulnerability_active(db: Session, key: str) -> bool:
        toggle = db.query(MockSandboxToggle).filter(MockSandboxToggle.key == key).first()
        return toggle.is_enabled if toggle else False

    @staticmethod
    def transfer_funds(db: Session, sender_acc_num: str, receiver_acc_num: str, amount: float, current_user_role: str = "USER") -> dict:
        idor_active = MockBankService.is_vulnerability_active(db, "VULN_IDOR_CROSS_ACCOUNT")
        neg_transfer_active = MockBankService.is_vulnerability_active(db, "VULN_NEGATIVE_TRANSFER")
        insufficient_bal_active = MockBankService.is_vulnerability_active(db, "VULN_INSUFFICIENT_BALANCE")
        duplicate_tx_active = MockBankService.is_vulnerability_active(db, "VULN_DUPLICATE_TX")

        sender = db.query(MockAccount).filter(MockAccount.account_number == sender_acc_num).first()
        receiver = db.query(MockAccount).filter(MockAccount.account_number == receiver_acc_num).first()

        if not sender:
            return {"success": False, "status_code": 404, "message": "Sender account not found"}
        if not receiver:
            return {"success": False, "status_code": 404, "message": "Receiver account not found"}

        # Negative transfer check
        if amount <= 0 and not neg_transfer_active:
            return {"success": False, "status_code": 400, "message": "Transfer amount must be positive"}

        # Insufficient balance check
        if sender.balance < amount and not insufficient_bal_active:
            return {"success": False, "status_code": 400, "message": "Insufficient account balance"}

        # Process transfer
        sender.balance -= amount
        receiver.balance += amount

        tx_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        tx = MockTransaction(
            transaction_id=tx_id,
            sender_account=sender.account_number,
            receiver_account=receiver.account_number,
            amount=amount,
            currency="INR",
            status="COMPLETED"
        )
        db.add(tx)
        db.commit()

        return {
            "success": True,
            "status_code": 200,
            "transaction_id": tx_id,
            "amount": amount,
            "sender_balance": sender.balance,
            "message": "Transfer executed successfully",
            "vulnerability_triggered": (amount <= 0 and neg_transfer_active) or (sender.balance < 0 and insufficient_bal_active)
        }
