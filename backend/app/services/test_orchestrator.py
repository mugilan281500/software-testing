from sqlalchemy.orm import Session
import datetime
import uuid
import time
from app.models import (
    TestCase, TestRun, TestResult, ApiTarget, Finding, AuditLog, MockSandboxToggle
)
from app.services.risk_engine import RiskEngine

class TestOrchestratorService:
    @staticmethod
    def get_adaptive_test_queue(db: Session) -> list:
        # Fetch all API targets sorted by risk level & regression priority
        apis = db.query(ApiTarget).all()
        
        priority_order = {"CRITICAL": 1, "HIGH": 2, "MEDIUM": 3, "LOW": 4}
        
        queue = []
        for api in apis:
            queue.append({
                "id": api.id,
                "name": api.name,
                "endpoint": api.endpoint,
                "method": api.method,
                "risk_level": api.risk_level,
                "risk_score": api.risk_score,
                "regression_priority": api.regression_priority,
                "priority_rank": priority_order.get(api.risk_level, 4)
            })

        # Sort queue: CRITICAL regression priority first, then highest risk level
        queue.sort(key=lambda x: (0 if x["regression_priority"] == "CRITICAL" else 1, x["priority_rank"], -x["risk_score"]))
        return queue

    @staticmethod
    def generate_negative_test_cases_for_endpoint(endpoint: str) -> list:
        # Generates 15 negative test case vectors per endpoint
        vectors = [
            ("NEG-001", "Missing Required Headers", "Authentication", "Missing Authorization Bearer Header", 401, {"error": "UNAUTHORIZED"}),
            ("NEG-002", "Expired JWT Token", "Authentication", "Sending expired Bearer token in request", 401, {"error": "TOKEN_EXPIRED"}),
            ("NEG-003", "Invalid Token Signature", "Authentication", "Sending forged/tampered JWT payload", 401, {"error": "INVALID_SIGNATURE"}),
            ("NEG-004", "BOLA / IDOR Cross-Account Access", "Authorization", "Accessing account number belonging to another user", 403, {"error": "FORBIDDEN"}),
            ("NEG-005", "Privilege Escalation Attempt", "Authorization", "Executing admin command with standard USER role", 403, {"error": "INSUFFICIENT_PERMISSIONS"}),
            ("NEG-006", "Negative Amount Transfer", "Banking Rules", "Passing amount = -5000 in payload", 400, {"error": "INVALID_AMOUNT"}),
            ("NEG-007", "Zero Amount Transfer", "Banking Rules", "Passing amount = 0 in payload", 400, {"error": "INVALID_AMOUNT"}),
            ("NEG-008", "Excessive Amount Above Balance", "Banking Rules", "Passing transfer amount > available balance", 400, {"error": "INSUFFICIENT_BALANCE"}),
            ("NEG-009", "Invalid Beneficiary Account", "Banking Rules", "Passing non-existent account string 'ACC-9999'", 404, {"error": "BENEFICIARY_NOT_FOUND"}),
            ("NEG-010", "Malformed JSON Payload", "Negative", "Sending unclosed JSON syntax", 400, {"error": "BAD_REQUEST"}),
            ("NEG-011", "String Type in Numeric Amount Field", "Negative", "Passing string 'FIVE_THOUSAND' for amount", 422, {"error": "UNPROCESSABLE_ENTITY"}),
            ("NEG-012", "SQL Injection Vector", "Security", "Injecting ' OR 1=1 -- in account field", 400, {"error": "INVALID_INPUT"}),
            ("NEG-013", "XSS Script Tag Payload", "Security", "Injecting <script>alert(1)</script> in note field", 400, {"error": "SANITY_CHECK_FAILED"}),
            ("NEG-014", "HTTP Rate Limit Spike", "Security", "Sending 100 requests in 1 second", 429, {"error": "TOO_MANY_REQUESTS"}),
            ("NEG-015", "Duplicate Idempotency Request", "Negative", "Sending identical transaction request concurrently", 409, {"error": "DUPLICATE_REQUEST"})
        ]
        return vectors

    @staticmethod
    def execute_test_suite(db: Session, selected_modules: list = None, trigger_source: str = "MANUAL") -> dict:
        start_time = time.time()
        run_number = f"RUN-{uuid.uuid4().hex[:6].upper()}"

        # Fetch active sandbox vulnerability toggles
        active_toggles = {t.key: t.is_enabled for t in db.query(MockSandboxToggle).all()}

        # Fetch all test cases
        all_test_cases = db.query(TestCase).all()

        if selected_modules:
            test_cases = [tc for tc in all_test_cases if tc.category in selected_modules]
        else:
            test_cases = all_test_cases

        results = []
        passed_count = 0
        failed_count = 0
        warning_count = 0
        critical_count = 0
        high_count = 0

        for tc in test_cases:
            # Determine pass/fail based on active sandbox toggles
            is_failed = False
            if tc.vulnerability_toggle_key and active_toggles.get(tc.vulnerability_toggle_key, False):
                is_failed = True  # Sandbox vulnerability active -> Test Fails!

            if is_failed:
                status = "FAIL"
                failed_count += 1
                risk = 90.0 if tc.severity == "CRITICAL" else (70.0 if tc.severity == "HIGH" else 45.0)
                if tc.severity == "CRITICAL":
                    critical_count += 1
                elif tc.severity == "HIGH":
                    high_count += 1
                
                # Check/create security finding
                finding = db.query(Finding).filter(Finding.finding_code == f"FIND-{tc.test_id}").first()
                if not finding:
                    finding = Finding(
                        finding_code=f"FIND-{tc.test_id}",
                        title=f"Vulnerability Detected: {tc.name}",
                        category=tc.category,
                        severity=tc.severity,
                        risk_score=risk,
                        api_endpoint=tc.endpoint,
                        status="OPEN",
                        evidence={"test_id": tc.test_id, "vulnerability_key": tc.vulnerability_toggle_key},
                        recommendation=f"Remediate security flaw for {tc.name} on endpoint {tc.endpoint}.",
                        cvss_score=9.1 if tc.severity == "CRITICAL" else 7.5
                    )
                    db.add(finding)
            else:
                status = "PASS"
                passed_count += 1
                risk = 0.0

            # Update test case status in DB
            tc.status = status

            tr = TestResult(
                test_case_id=tc.test_id,
                test_name=tc.name,
                category=tc.category,
                api_endpoint=tc.endpoint,
                status=status,
                severity=tc.severity,
                risk_score=risk,
                actual_status=tc.expected_status if status == "PASS" else 200,
                response_time_ms=round(35.0 + (len(tc.name) % 15), 1),
                evidence={
                    "expected_status": tc.expected_status,
                    "actual_status": tc.expected_status if status == "PASS" else 200,
                    "validation": "PASS" if status == "PASS" else "VULNERABILITY_CONFIRMED",
                    "response_time_ms": 35.0
                },
                recommendation=f"Ensure strict {tc.category} controls on {tc.endpoint}."
            )
            results.append(tr)

        duration_ms = round((time.time() - start_time) * 1000.0, 1)
        overall_risk, sec_score = RiskEngine.calculate_overall_risk(results)

        test_run = TestRun(
            run_number=run_number,
            execution_type="SELECTED" if selected_modules else "FULL_SUITE",
            total_tests=len(results),
            passed=passed_count,
            failed=failed_count,
            warning_count=warning_count,
            critical_count=critical_count,
            high_count=high_count,
            overall_risk_score=overall_risk,
            security_score=sec_score,
            duration_ms=duration_ms,
            status="COMPLETED",
            executed_by="ADMIN",
            trigger_source=trigger_source,
            results=results
        )
        db.add(test_run)

        # Audit Log
        audit = AuditLog(
            user_email="tester@banksecure.io",
            action="SECURITY_TEST",
            resource=f"TEST_RUN-{run_number}",
            result="SUCCESS",
            risk_score=overall_risk,
            details={
                "run_number": run_number,
                "total": len(results),
                "passed": passed_count,
                "failed": failed_count,
                "modules": selected_modules or "ALL"
            }
        )
        db.add(audit)
        db.commit()
        db.refresh(test_run)

        return {
            "run_number": run_number,
            "total_tests": len(results),
            "passed": passed_count,
            "failed": failed_count,
            "critical_count": critical_count,
            "high_count": high_count,
            "overall_risk_score": overall_risk,
            "security_score": sec_score,
            "duration_ms": duration_ms,
            "execution_type": test_run.execution_type,
            "status": "COMPLETED"
        }
