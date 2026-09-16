import uuid
import datetime
from sqlalchemy.orm import Session
from app.models import ApiTarget, TestCase, TestRun, TestResult, Finding, ThreatFlag, RiskHistory

class SmartAnalytics:
    @staticmethod
    def get_release_readiness(db: Session) -> dict:
        latest_run = db.query(TestRun).order_by(TestRun.id.desc()).first()
        critical_count = db.query(Finding).filter(Finding.severity == "CRITICAL", Finding.status == "OPEN").count()
        high_count = db.query(Finding).filter(Finding.severity == "HIGH", Finding.status == "OPEN").count()
        
        overall_risk = latest_run.overall_risk_score if latest_run else 87.5
        security_score = latest_run.security_score if latest_run else 12.5

        # Quality Gate condition: FAIL if critical > 0 or risk > 50
        is_gate_passed = (critical_count == 0 and overall_risk <= 50.0)

        # Requirement Coverage
        total_apis = db.query(ApiTarget).count()
        total_cases = db.query(TestCase).count()
        
        category_coverage = {
            "Authentication": 95.0,
            "Authorization": 88.0,
            "Business Logic": 82.0,
            "Validation": 90.0,
            "Security Headers": 100.0,
            "Rate Limiting": 75.0,
            "Response Validation": 85.0
        }

        # Flaky test detection (simulated consistency score)
        flaky_tests = [
            {"test_id": "RATE-001", "name": "100 Rapid Requests Throttling Test", "flakiness_score": "12%", "reason": "Network latency jitter"},
            {"test_id": "LOGIC-003", "name": "Zero Amount Fund Transfer", "flakiness_score": "4%", "reason": "Intermittent mock lock"}
        ]

        # Test Impact Analysis
        impact_analysis = {
            "affected_apis": total_apis,
            "high_priority_tests": [tc.test_id for tc in db.query(TestCase).filter(TestCase.severity.in_(["CRITICAL", "HIGH"])).all()[:5]],
            "recommended_run_scope": "SECURITY_REGRESSION" if critical_count > 0 else "FULL_SUITE"
        }

        return {
            "status": "APPROVED FOR RELEASE" if is_gate_passed else "RELEASE BLOCKED",
            "is_gate_passed": is_gate_passed,
            "quality_gate_policy": "Fail on ANY Critical Finding or Dynamic Risk > 50.0",
            "security_score": security_score,
            "overall_risk_score": overall_risk,
            "open_defects": {
                "critical": critical_count,
                "high": high_count,
                "total_open": db.query(Finding).filter(Finding.status == "OPEN").count()
            },
            "requirement_coverage": category_coverage,
            "total_test_vectors": total_cases,
            "flaky_tests": flaky_tests,
            "test_impact_analysis": impact_analysis
        }

    @staticmethod
    def auto_generate_tests_for_api(db: Session, api_id: int) -> list:
        target = db.query(ApiTarget).filter(ApiTarget.id == api_id).first()
        if not target:
            return []

        endpoint = target.endpoint
        name = target.name

        generated = [
            TestCase(
                test_id=f"AUTO-AUTH-{uuid.uuid4().hex[:4].upper()}",
                name=f"Auto Auth Bypass: {name}",
                category="Authentication",
                description=f"Automated token signature tampering assertion for {endpoint}",
                request_method=target.method,
                endpoint=endpoint,
                expected_status=401,
                expected_result="HTTP 401 Unauthorized",
                severity="CRITICAL",
                vulnerability_toggle_key="VULN_EXPIRED_JWT"
            ),
            TestCase(
                test_id=f"AUTO-LOGIC-{uuid.uuid4().hex[:4].upper()}",
                name=f"Auto Boundary Negative Test: {name}",
                category="Negative Testing",
                description=f"Automated payload boundary negative test for {endpoint}",
                request_method=target.method,
                endpoint=endpoint,
                expected_status=400,
                expected_result="HTTP 400 Bad Request",
                severity="HIGH",
                vulnerability_toggle_key="VULN_NEGATIVE_TRANSFER"
            ),
            TestCase(
                test_id=f"AUTO-HEAD-{uuid.uuid4().hex[:4].upper()}",
                name=f"Auto Header Assertion: {name}",
                category="Security Headers",
                description=f"Automated HSTS and CSP header presence test for {endpoint}",
                request_method="GET",
                endpoint=endpoint,
                expected_status=200,
                expected_result="Headers present",
                severity="MEDIUM",
                vulnerability_toggle_key="VULN_MISSING_HEADERS"
            )
        ]

        db.add_all(generated)
        db.commit()
        return generated
