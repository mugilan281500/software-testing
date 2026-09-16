from sqlalchemy.orm import Session
import datetime
import uuid
from app.models import (
    MockAccount, MockTransaction, TransactionSecurityEvent, TransactionRiskScore,
    SecurityAlert, AuditLog, LoginAttempt, RiskRule
)
from app.services.behavior_baseline import BehaviorBaselineService
from app.services.banking_rule_engine import BankingRuleEngine
from app.services.correlation_engine import MultiEventCorrelationEngine
from app.services.auto_test_trigger import AutoSecurityTestTriggerService

class RealTimeTransactionMonitorEngine:
    @staticmethod
    def monitor_transaction(
        db: Session,
        sender_acc_num: str,
        receiver_acc_num: str,
        amount: float,
        currency: str = "INR",
        device_id: str = "DEVICE-001",
        ip_address: str = "192.168.1.50"
    ) -> dict:
        now = datetime.datetime.utcnow()

        # 1. Fetch Account Details
        sender = db.query(MockAccount).filter(MockAccount.account_number == sender_acc_num).first()
        receiver = db.query(MockAccount).filter(MockAccount.account_number == receiver_acc_num).first()

        # 2. Evaluate Banking Business Rules
        rule_eval = BankingRuleEngine.evaluate_rules(db, sender_acc_num, receiver_acc_num, amount, currency)

        # 3. Evaluate User Behavior Baseline (Amount, Device, IP, Time)
        baseline_indicators = BehaviorBaselineService.evaluate_transaction_against_baseline(
            db, sender_acc_num, amount, device_id, ip_address, now
        )

        indicators = []
        indicators.extend(baseline_indicators)

        # 4. Check Rapid Transactions (Frequency in last 2 minutes)
        two_mins_ago = now - datetime.timedelta(minutes=2)
        recent_tx_count = db.query(MockTransaction).filter(
            MockTransaction.sender_account == sender_acc_num,
            MockTransaction.timestamp >= two_mins_ago
        ).count()

        if recent_tx_count >= 2:
            indicators.append({
                "code": "IND-FREQ-RAPID",
                "name": "Multiple Transactions in Short Period",
                "severity": "HIGH" if recent_tx_count >= 4 else "MEDIUM",
                "points": 20.0,
                "explanation": f"Rapid execution detected: {recent_tx_count + 1} transactions requested within a 2-minute window."
            })

        # 5. Check Repeated Authentication Failures
        username = f"user_{sender_acc_num[-4:]}" if sender_acc_num else "user"
        failed_logins = db.query(LoginAttempt).filter(
            LoginAttempt.username == username,
            LoginAttempt.status == "FAILED",
            LoginAttempt.timestamp >= (now - datetime.timedelta(minutes=15))
        ).count()

        if failed_logins >= 2:
            indicators.append({
                "code": "IND-AUTH-FAIL",
                "name": "Repeated Authentication Failures",
                "severity": "HIGH",
                "points": 15.0,
                "explanation": f"Recent authentication anomaly: {failed_logins} failed login attempt(s) recorded within past 15 minutes."
            })

        # 6. Check Banking Rule Violation Penalties
        for br in rule_eval["rule_results"]:
            if br["status"] in ["FAIL", "WARNING"] and br["penalty"] > 0:
                indicators.append({
                    "code": f"IND-RULE-{br['code']}",
                    "name": f"Business Rule Violation ({br['rule']})",
                    "severity": "HIGH" if br["status"] == "FAIL" else "MEDIUM",
                    "points": br["penalty"],
                    "explanation": br["message"]
                })

        # 7. Check Duplicate Transaction Flag
        duplicate_flag = any(r["code"] == "RULE-DUPLICATE-TX" and r["status"] == "WARNING" for r in rule_eval["rule_results"])
        if duplicate_flag and not any(i["code"] == "IND-DUP-TX" for i in indicators):
            indicators.append({
                "code": "IND-DUP-TX",
                "name": "Duplicate Transaction Detected",
                "severity": "MEDIUM",
                "points": 15.0,
                "explanation": f"Identical transaction of ₹{amount:,.2f} to beneficiary {receiver_acc_num} requested in close succession."
            })

        # 8. Check Sudden Baseline Shift / Extreme Outlier
        profile = BehaviorBaselineService.get_or_create_profile(db, sender_acc_num)
        if amount > (profile.avg_amount * 5.0):
            indicators.append({
                "code": "IND-BASELINE-SHIFT",
                "name": "Sudden Change from Normal User Behavior",
                "severity": "CRITICAL",
                "points": 20.0,
                "explanation": f"Sudden structural shift: Transaction amount (₹{amount:,.2f}) is >5x historical mean baseline."
            })

        # 9. Calculate Overall Transaction Risk Score (0 - 100)
        base_score = sum(ind["points"] for ind in indicators)

        # 10. Check Risk Escalation across sequential transactions
        last_3_txs = db.query(MockTransaction).filter(
            MockTransaction.sender_account == sender_acc_num
        ).order_by(MockTransaction.id.desc()).limit(3).all()

        risk_escalation_detected = False
        if len(last_3_txs) >= 2:
            scores = [tx.risk_score for tx in reversed(last_3_txs)]
            # Check if scores are strictly increasing
            if all(x < y for x, y in zip(scores, scores[1:])):
                risk_escalation_detected = True
                base_score += 15.0
                indicators.append({
                    "code": "IND-RISK-ESCALATION",
                    "name": "Risk Escalation Sequence Detected",
                    "severity": "HIGH",
                    "points": 15.0,
                    "explanation": f"Continuous risk escalation detected across sequential transactions: {[round(s, 1) for s in scores]} -> +15.0 escalation penalty."
                })

        final_risk_score = round(min(100.0, max(0.0, base_score)), 1)

        # Determine Risk Level
        if final_risk_score >= 80.0:
            risk_level = "CRITICAL"
            decision = "BLOCKED"
        elif final_risk_score >= 60.0:
            risk_level = "HIGH"
            decision = "REVIEW"
        elif final_risk_score >= 30.0:
            risk_level = "MEDIUM"
            decision = "MONITOR"
        else:
            risk_level = "LOW"
            decision = "ALLOWED"

        # Force block if banking rule hard fails (e.g. negative amount, sender blocked, zero balance)
        if rule_eval["is_blocked"]:
            decision = "BLOCKED"
            if final_risk_score < 80.0:
                final_risk_score = max(final_risk_score, 80.0)
                risk_level = "CRITICAL"

        # 11. Create & Save Transaction Record
        tx_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
        tx_status = "COMPLETED" if decision in ["ALLOWED", "MONITOR"] else ("REVIEW" if decision == "REVIEW" else "REJECTED")

        transaction = MockTransaction(
            transaction_id=tx_id,
            sender_account=sender_acc_num,
            receiver_account=receiver_acc_num,
            amount=amount,
            currency=currency,
            status=tx_status,
            type="TRANSFER",
            device_id=device_id,
            ip_address=ip_address,
            timestamp=now,
            risk_score=final_risk_score,
            risk_level=risk_level,
            decision=decision,
            flags_count=len(indicators)
        )
        db.add(transaction)

        # 12. Create Security Events
        for ind in indicators:
            evt = TransactionSecurityEvent(
                transaction_id=tx_id,
                indicator_code=ind["code"],
                indicator_name=ind["name"],
                severity=ind["severity"],
                score_impact=ind["points"],
                explanation=ind["explanation"]
            )
            db.add(evt)

        # 13. Create Transaction Security Scorecard (6 categories: Auth, Authz, Validation, Business Rules, Behavior, API Sec)
        auth_score = 100.0 if failed_logins == 0 else max(30.0, 100.0 - (failed_logins * 25.0))
        authz_score = 100.0 if not sender or not sender.is_blocked else 20.0
        val_score = 100.0 if amount > 0 else 0.0
        br_score = rule_eval["compliance_score"]
        behavior_score = round(max(0.0, 100.0 - (len(baseline_indicators) * 20.0)), 1)
        api_sec_score = round(max(0.0, 100.0 - final_risk_score), 1)

        factors_json = [
            {
                "code": ind["code"],
                "factor": ind["name"],
                "points": f"+{int(ind['points'])}",
                "explanation": ind["explanation"],
                "severity": ind["severity"]
            }
            for ind in indicators
        ]

        scorecard = TransactionRiskScore(
            transaction_id=tx_id,
            overall_score=final_risk_score,
            risk_level=risk_level,
            decision=decision,
            auth_score=auth_score,
            authz_score=authz_score,
            validation_score=val_score,
            business_rules_score=br_score,
            behavior_score=behavior_score,
            api_security_score=api_sec_score,
            factors_json=factors_json
        )
        db.add(scorecard)

        # 14. If transfer is allowed/monitored and balance check passed, update balances
        if decision in ["ALLOWED", "MONITOR"] and sender and receiver and sender.balance >= amount and amount > 0:
            sender.balance -= amount
            receiver.balance += amount

        # 15. Create Alert if Risk >= HIGH (>=60)
        if final_risk_score >= 60.0:
            alert = SecurityAlert(
                alert_code=f"ALT-{uuid.uuid4().hex[:6].upper()}",
                title=f"{risk_level} Transaction Risk Alert [{tx_id}]",
                severity=risk_level,
                endpoint="/mock-bank/transfer",
                transaction_id=tx_id,
                message=f"Transaction {tx_id} scored {final_risk_score}/100 ({risk_level}). Decision: {decision}. Flags: {len(indicators)}.",
                status="ACTIVE",
                risk_score=final_risk_score
            )
            db.add(alert)

        # 16. Audit Log
        audit = AuditLog(
            user_email=f"user_{sender_acc_num[-4:]}@banksecure.io" if sender_acc_num else "customer@banksecure.io",
            action="TRANSACTION_STARTED" if decision == "ALLOWED" else "TRANSACTION_FLAGGED",
            resource=f"TXN-{tx_id}",
            result=decision,
            risk_score=final_risk_score,
            details={
                "sender": sender_acc_num,
                "receiver": receiver_acc_num,
                "amount": amount,
                "decision": decision,
                "risk_score": final_risk_score,
                "indicators": [i["name"] for i in indicators]
            }
        )
        db.add(audit)
        db.commit()
        db.refresh(transaction)

        # 17. Multi-Event Correlation Check
        correlated_incident = MultiEventCorrelationEngine.check_and_correlate(db, sender_acc_num, transaction)

        # 18. Auto-Trigger Security Tests if HIGH or CRITICAL risk
        auto_test_res = AutoSecurityTestTriggerService.trigger_security_tests_if_high_risk(db, transaction)

        return {
            "success": decision != "BLOCKED",
            "transaction_id": tx_id,
            "amount": amount,
            "sender_account": sender_acc_num,
            "receiver_account": receiver_acc_num,
            "sender_balance": sender.balance if sender else 0.0,
            "risk_score": final_risk_score,
            "risk_level": risk_level,
            "decision": decision,
            "flags_count": len(indicators),
            "indicators": indicators,
            "scorecard": {
                "auth_score": auth_score,
                "authz_score": authz_score,
                "validation_score": val_score,
                "business_rules_score": br_score,
                "behavior_score": behavior_score,
                "api_security_score": api_sec_score,
                "overall_score": final_risk_score
            },
            "risk_escalation_detected": risk_escalation_detected,
            "correlated_incident": correlated_incident.incident_code if correlated_incident else None,
            "auto_triggered_tests": auto_test_res,
            "message": f"Transaction processed: Decision={decision}, Risk Score={final_risk_score}/100 ({risk_level})"
        }
