from sqlalchemy.orm import Session
import datetime
from app.models import MockAccount, MockBeneficiary, MockTransaction, BankingRule

class BankingRuleEngine:
    @staticmethod
    def evaluate_rules(db: Session, sender_acc_num: str, receiver_acc_num: str, amount: float, currency: str = "INR") -> dict:
        sender = db.query(MockAccount).filter(MockAccount.account_number == sender_acc_num).first()
        receiver = db.query(MockAccount).filter(MockAccount.account_number == receiver_acc_num).first()
        
        results = []
        is_blocked_tx = False
        total_risk_penalty = 0.0

        # Fetch configured rules from DB or fallback
        rules = db.query(BankingRule).all()
        enabled_rule_codes = {r.rule_code: r for r in rules if r.is_enabled}

        # 1. Account Status Rule
        rule_status = enabled_rule_codes.get("RULE-ACCOUNT-STATUS")
        if sender and sender.is_blocked:
            is_blocked_tx = True
            total_risk_penalty += 30.0
            results.append({
                "rule": "Account Status",
                "code": "RULE-ACCOUNT-STATUS",
                "status": "FAIL",
                "message": "Sender account is blocked or frozen.",
                "penalty": 30.0
            })
        else:
            results.append({
                "rule": "Account Status",
                "code": "RULE-ACCOUNT-STATUS",
                "status": "PASS",
                "message": "Sender account is active and verified.",
                "penalty": 0.0
            })

        # 2. Transaction Amount Bounds Rule (Positive & >0)
        rule_amt = enabled_rule_codes.get("RULE-AMOUNT-BOUNDS")
        if amount <= 0:
            is_blocked_tx = True
            total_risk_penalty += 35.0
            results.append({
                "rule": "Transaction Amount Bounds",
                "code": "RULE-AMOUNT-BOUNDS",
                "status": "FAIL",
                "message": "Transfer amount must be greater than 0.",
                "penalty": 35.0
            })
        else:
            results.append({
                "rule": "Transaction Amount Bounds",
                "code": "RULE-AMOUNT-BOUNDS",
                "status": "PASS",
                "message": "Transfer amount is valid and positive.",
                "penalty": 0.0
            })

        # 3. Account Balance Check Rule
        rule_bal = enabled_rule_codes.get("RULE-BALANCE-CHECK")
        if sender and sender.balance < amount:
            is_blocked_tx = True
            total_risk_penalty += 25.0
            results.append({
                "rule": "Balance Check",
                "code": "RULE-BALANCE-CHECK",
                "status": "FAIL",
                "message": f"Requested amount (₹{amount:,.2f}) exceeds current account balance (₹{sender.balance:,.2f}).",
                "penalty": 25.0
            })
        else:
            results.append({
                "rule": "Balance Check",
                "code": "RULE-BALANCE-CHECK",
                "status": "PASS",
                "message": "Account balance is sufficient.",
                "penalty": 0.0
            })

        # 4. Minimum Required Balance Rule (e.g. ₹1,000)
        rule_min = enabled_rule_codes.get("RULE-MIN-BALANCE")
        min_balance = rule_min.threshold_value if rule_min else 1000.0
        if sender and (sender.balance - amount) < min_balance and amount > 0 and sender.balance >= amount:
            total_risk_penalty += 15.0
            results.append({
                "rule": "Minimum Balance Limit",
                "code": "RULE-MIN-BALANCE",
                "status": "WARNING",
                "message": f"Transfer will reduce account balance below minimum required threshold (₹{min_balance:,.2f}).",
                "penalty": 15.0
            })
        elif sender and sender.balance >= amount:
            results.append({
                "rule": "Minimum Balance Limit",
                "code": "RULE-MIN-BALANCE",
                "status": "PASS",
                "message": "Minimum account balance maintained.",
                "penalty": 0.0
            })

        # 5. Daily Transfer Limit Rule
        rule_limit = enabled_rule_codes.get("RULE-DAILY-LIMIT")
        daily_limit = sender.daily_limit if sender else 100000.0
        # Calculate sum of today's transfers
        today_start = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        today_txs_sum = sum(
            tx.amount for tx in db.query(MockTransaction).filter(
                MockTransaction.sender_account == sender_acc_num,
                MockTransaction.timestamp >= today_start,
                MockTransaction.status.in_(["COMPLETED", "MONITOR", "REVIEW"])
            ).all()
        )
        if (today_txs_sum + amount) > daily_limit:
            total_risk_penalty += 20.0
            results.append({
                "rule": "Daily Transfer Limit",
                "code": "RULE-DAILY-LIMIT",
                "status": "FAIL" if (today_txs_sum + amount) > (daily_limit * 1.5) else "WARNING",
                "message": f"Daily cumulative transfers (₹{(today_txs_sum + amount):,.2f}) exceed daily limit (₹{daily_limit:,.2f}).",
                "penalty": 20.0
            })
        else:
            results.append({
                "rule": "Daily Transfer Limit",
                "code": "RULE-DAILY-LIMIT",
                "status": "PASS",
                "message": "Daily transfer limit compliant.",
                "penalty": 0.0
            })

        # 6. Beneficiary Validation Rule
        rule_ben = enabled_rule_codes.get("RULE-BENEFICIARY")
        beneficiary = db.query(MockBeneficiary).filter(
            MockBeneficiary.account_number == sender_acc_num,
            MockBeneficiary.beneficiary_account == receiver_acc_num
        ).first()
        if not beneficiary and receiver_acc_num != sender_acc_num:
            total_risk_penalty += 15.0
            results.append({
                "rule": "Beneficiary Validation",
                "code": "RULE-BENEFICIARY",
                "status": "WARNING",
                "message": f"Beneficiary account '{receiver_acc_num}' is not in sender saved verified beneficiary list.",
                "penalty": 15.0
            })
        else:
            results.append({
                "rule": "Beneficiary Validation",
                "code": "RULE-BENEFICIARY",
                "status": "PASS",
                "message": "Beneficiary is verified.",
                "penalty": 0.0
            })

        # 7. Currency Validation Rule
        rule_curr = enabled_rule_codes.get("RULE-CURRENCY")
        if currency.upper() not in ["INR", "USD", "EUR"]:
            total_risk_penalty += 10.0
            results.append({
                "rule": "Currency Validation",
                "code": "RULE-CURRENCY",
                "status": "FAIL",
                "message": f"Unsupported transaction currency '{currency}'.",
                "penalty": 10.0
            })
        else:
            results.append({
                "rule": "Currency Validation",
                "code": "RULE-CURRENCY",
                "status": "PASS",
                "message": "Transaction currency valid.",
                "penalty": 0.0
            })

        # 8. Duplicate Transaction Rule (same amount, sender, receiver within 2 minutes)
        two_mins_ago = datetime.datetime.utcnow() - datetime.timedelta(minutes=2)
        duplicate_tx = db.query(MockTransaction).filter(
            MockTransaction.sender_account == sender_acc_num,
            MockTransaction.receiver_account == receiver_acc_num,
            MockTransaction.amount == amount,
            MockTransaction.timestamp >= two_mins_ago
        ).first()

        if duplicate_tx:
            total_risk_penalty += 25.0
            results.append({
                "rule": "Duplicate Transaction Check",
                "code": "RULE-DUPLICATE-TX",
                "status": "WARNING",
                "message": f"Identical transaction (₹{amount:,.2f} to {receiver_acc_num}) detected within the past 2 minutes.",
                "penalty": 25.0
            })
        else:
            results.append({
                "rule": "Duplicate Transaction Check",
                "code": "RULE-DUPLICATE-TX",
                "status": "PASS",
                "message": "No duplicate transaction detected.",
                "penalty": 0.0
            })

        # Calculate overall business compliance score (0-100)
        passed_count = sum(1 for r in results if r["status"] == "PASS")
        compliance_score = round((passed_count / float(len(results))) * 100.0, 1)

        return {
            "is_blocked": is_blocked_tx,
            "compliance_score": compliance_score,
            "total_penalty": total_risk_penalty,
            "rule_results": results
        }
