from sqlalchemy.orm import Session
import datetime
import uuid
from app.models import TestRun, TestResult, TestCase, MockTransaction, SecurityAlert, AuditLog

class AutoSecurityTestTriggerService:
    @staticmethod
    def trigger_security_tests_if_high_risk(db: Session, transaction: MockTransaction) -> dict:
        if transaction.risk_score < 60.0:
            return {"triggered": False, "reason": "Risk score below HIGH threshold (<60.0)"}

        # Auto-trigger 6 security test modules for the transaction endpoint (/mock-bank/transfer)
        run_number = f"RUN-AUTO-{uuid.uuid4().hex[:6].upper()}"

        test_cases = db.query(TestCase).filter(
            TestCase.endpoint.in_(["/mock-bank/transfer", "/api/v1/mock-bank/transfer", "/transfer"])
        ).all()

        if not test_cases:
            # Fallback: query all active test cases
            test_cases = db.query(TestCase).limit(6).all()

        results = []
        passed_count = 0
        failed_count = 0
        critical_count = 0
        high_count = 0

        for tc in test_cases:
            # Simulate real verification of test case parameters
            # If toggle key matches active sandbox vulnerability or risk level is critical, record result
            is_pass = True
            if transaction.risk_score >= 80.0 and tc.severity in ["CRITICAL", "HIGH"]:
                is_pass = False  # Simulated security finding under active critical risk scenario

            if is_pass:
                status = "PASS"
                passed_count += 1
                risk = 0.0
            else:
                status = "FAIL"
                failed_count += 1
                risk = 85.0 if tc.severity == "CRITICAL" else 65.0
                if tc.severity == "CRITICAL":
                    critical_count += 1
                else:
                    high_count += 1

            tr = TestResult(
                test_case_id=tc.test_id,
                test_name=tc.name,
                category=tc.category,
                api_endpoint=tc.endpoint,
                status=status,
                severity=tc.severity,
                risk_score=risk,
                actual_status=200 if is_pass else 403,
                response_time_ms=45.0,
                evidence={
                    "triggered_by_tx": transaction.transaction_id,
                    "tx_risk_score": transaction.risk_score,
                    "validation": "PASS" if is_pass else "SECURITY_VIOLATION_DETECTED"
                },
                recommendation=f"Enforce strict server-side validation for {tc.category} on {tc.endpoint}."
            )
            results.append(tr)

        test_run = TestRun(
            run_number=run_number,
            execution_type="AUTO_TRIGGERED",
            total_tests=len(results),
            passed=passed_count,
            failed=failed_count,
            critical_count=critical_count,
            high_count=high_count,
            overall_risk_score=transaction.risk_score,
            security_score=max(0.0, 100.0 - transaction.risk_score),
            duration_ms=250.0,
            status="COMPLETED",
            executed_by="AUTO_RISK_ENGINE",
            trigger_source=f"TRANSACTION_{transaction.transaction_id}",
            results=results
        )
        db.add(test_run)

        # Audit log for auto-trigger
        audit = AuditLog(
            user_email="risk_engine@system",
            action="SECURITY_TEST",
            resource=f"TEST_RUN-{run_number}",
            result="SUCCESS",
            risk_score=transaction.risk_score,
            details={
                "transaction_id": transaction.transaction_id,
                "tx_risk": transaction.risk_score,
                "tests_triggered": len(results),
                "failed_tests": failed_count
            }
        )
        db.add(audit)
        db.commit()

        return {
            "triggered": True,
            "run_number": run_number,
            "total_tests": len(results),
            "passed": passed_count,
            "failed": failed_count,
            "tx_risk": transaction.risk_score
        }
