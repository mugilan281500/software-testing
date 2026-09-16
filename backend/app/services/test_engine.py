import datetime
import uuid
import httpx
from sqlalchemy.orm import Session
from app.models import TestCase, TestRun, TestResult, Finding, ThreatFlag, MockSandboxToggle, AuditLog
from app.services.risk_engine import RiskEngine

REMEDIATION_GUIDE = {
    "Authentication": "Validate JWT signature, issuer, audience, and expiration strictly on every request. Disallow unauthenticated or expired tokens.",
    "Authorization": "Enforce strict server-side Object-Level Authorization (RBAC/ABAC). Verify that the authenticated user owns the requested account/resource.",
    "Business Logic": "Implement thorough domain validation logic on the server side before executing financial operations. Reject negative/zero transfers and enforce atomic locks.",
    "Validation": "Sanitize and validate all incoming payload fields, data types, and boundaries before processing.",
    "Rate Limiting": "Configure rate-limiting throttling (e.g. 30 requests/minute per IP/User) at the API Gateway or application level.",
    "Security Headers": "Add missing security headers: Strict-Transport-Security, Content-Security-Policy, X-Content-Type-Options, X-Frame-Options, Cache-Control.",
    "Response Validation": "Filter sensitive fields (passwords, tokens, internal IDs, stack traces) from API responses before returning data."
}

class TestEngine:
    @staticmethod
    def run_suite(db: Session, execution_type: str = "FULL_SUITE", target_endpoint: str = None, executed_by: str = "ADMIN") -> TestRun:
        run_number = f"RUN-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        
        query = db.query(TestCase)
        if target_endpoint:
            query = query.filter(TestCase.endpoint == target_endpoint)
        
        test_cases = query.all()
        
        test_run = TestRun(
            run_number=run_number,
            execution_type=execution_type,
            total_tests=len(test_cases),
            status="RUNNING",
            executed_by=executed_by,
            started_at=datetime.datetime.utcnow()
        )
        db.add(test_run)
        db.commit()
        db.refresh(test_run)

        passed_count = 0
        failed_count = 0
        critical_count = 0
        high_count = 0
        results = []

        for tc in test_cases:
            # Evaluate test case against current mock sandbox state
            is_vuln_active = False
            if tc.vulnerability_toggle_key:
                toggle = db.query(MockSandboxToggle).filter(MockSandboxToggle.key == tc.vulnerability_toggle_key).first()
                if toggle and toggle.is_enabled:
                    is_vuln_active = True

            # If vulnerability toggle is ENABLED in sandbox, test FAILS (vulnerability exposed!)
            # If toggle is DISABLED (secured), test PASSES!
            if is_vuln_active:
                status = "FAILED"
                failed_count += 1
                actual_status = 200 if tc.expected_status in [401, 403, 400, 429] else 500
                evidence = {
                    "request_method": tc.request_method,
                    "endpoint": tc.endpoint,
                    "expected_status": tc.expected_status,
                    "actual_status": actual_status,
                    "vulnerability_flag": tc.vulnerability_toggle_key,
                    "details": f"Vulnerability detected: API accepted unauthorized or invalid input under test condition [{tc.name}]"
                }
                if tc.severity == "CRITICAL":
                    critical_count += 1
                elif tc.severity == "HIGH":
                    high_count += 1
            else:
                status = "PASSED"
                passed_count += 1
                actual_status = tc.expected_status
                evidence = {
                    "request_method": tc.request_method,
                    "endpoint": tc.endpoint,
                    "expected_status": tc.expected_status,
                    "actual_status": actual_status,
                    "details": "Request properly rejected or authorized as expected."
                }

            risk_score = RiskEngine.calculate_test_risk(tc.severity, tc.category, status == "PASSED")
            rec = REMEDIATION_GUIDE.get(tc.category, "Enforce strict security validation.")

            result = TestResult(
                test_run_id=test_run.id,
                test_case_id=tc.test_id,
                test_name=tc.name,
                category=tc.category,
                api_endpoint=tc.endpoint,
                status=status,
                severity=tc.severity,
                risk_score=risk_score,
                actual_status=actual_status,
                evidence=evidence,
                recommendation=rec
            )
            db.add(result)
            results.append(result)

            # Auto-generate Finding and Threat Flag if FAILED
            if status == "FAILED":
                TestEngine._generate_finding_and_flag(db, tc, evidence, risk_score, rec)

        db.commit()

        overall_risk, security_score = RiskEngine.calculate_overall_risk(results)

        test_run.passed = passed_count
        test_run.failed = failed_count
        test_run.critical_count = critical_count
        test_run.high_count = high_count
        test_run.overall_risk_score = overall_risk
        test_run.security_score = security_score
        test_run.status = "COMPLETED"
        test_run.completed_at = datetime.datetime.utcnow()

        # Audit Log
        audit = AuditLog(
            user_email=executed_by,
            action="EXECUTE_SECURITY_SUITE",
            resource=f"TestRun:{run_number}",
            result="COMPLETED",
            risk_score=overall_risk,
            details={"passed": passed_count, "failed": failed_count, "security_score": security_score}
        )
        db.add(audit)

        db.commit()
        db.refresh(test_run)
        return test_run

    @staticmethod
    def run_custom_test(db: Session, req_data: dict, executed_by: str = "ADMIN") -> dict:
        api_name = req_data.get("api_name", "Custom API Target")
        api_url = req_data.get("api_url")
        method = req_data.get("method", "GET").upper()
        auth_type = req_data.get("auth_type", "NONE")
        auth_token = req_data.get("auth_token")
        headers = req_data.get("headers") or {}
        parameters = req_data.get("parameters") or {}
        payload = req_data.get("payload") or {}
        expected_status = req_data.get("expected_status", 200)

        # Prepare HTTP headers
        req_headers = {**headers}
        if auth_type == "BEARER_JWT" and auth_token:
            req_headers["Authorization"] = f"Bearer {auth_token}"
        elif auth_type == "API_KEY" and auth_token:
            req_headers["X-API-Key"] = auth_token

        # Send actual HTTP request
        actual_status = 500
        response_text = ""
        response_headers = {}
        response_time_ms = 0
        error_detail = None

        try:
            start_time = datetime.datetime.utcnow()
            with httpx.Client(timeout=10.0, follow_redirects=True) as client:
                res = client.request(
                    method=method,
                    url=api_url,
                    headers=req_headers,
                    params=parameters,
                    json=payload if payload else None
                )
                end_time = datetime.datetime.utcnow()
                response_time_ms = round((end_time - start_time).total_seconds() * 1000, 2)
                actual_status = res.status_code
                response_text = res.text[:2000]  # Cap snippet
                response_headers = dict(res.headers)
        except Exception as e:
            error_detail = str(e)
            actual_status = 500

        # Multi-Vector Evaluation
        vector_findings = []
        
        # 1. Status Assertion
        status_passed = (actual_status == expected_status)
        if not status_passed:
            vector_findings.append({
                "vector": "Functional / HTTP Status",
                "severity": "HIGH",
                "issue": f"Expected HTTP {expected_status}, received HTTP {actual_status}.",
                "recommendation": "Verify API endpoint status code configuration and payload schema."
            })

        # 2. Security Headers
        missing_headers = []
        if "strict-transport-security" not in [h.lower() for h in response_headers.keys()]:
            missing_headers.append("Strict-Transport-Security")
        if "content-security-policy" not in [h.lower() for h in response_headers.keys()]:
            missing_headers.append("Content-Security-Policy")

        if missing_headers:
            vector_findings.append({
                "vector": "Security Headers",
                "severity": "MEDIUM",
                "issue": f"Missing critical headers: {', '.join(missing_headers)}",
                "recommendation": "Configure Strict-Transport-Security and Content-Security-Policy headers on API Gateway."
            })

        # 3. Sensitive Data Leakage Check
        lower_resp = response_text.lower()
        if "password_hash" in lower_resp or "secret_key" in lower_resp or "traceback" in lower_resp:
            vector_findings.append({
                "vector": "Data Protection / Data Leakage",
                "severity": "CRITICAL",
                "issue": "API response contains potential sensitive internal data or unhandled stack trace.",
                "recommendation": "Mask confidential fields and disable verbose debug error outputs."
            })

        # Calculate Dynamic Risk Score
        is_overall_pass = (len(vector_findings) == 0 and status_passed)
        if is_overall_pass:
            risk_score = 12.0
            severity = "LOW"
            status = "PASSED"
        else:
            highest_sev = "CRITICAL" if any(v["severity"] == "CRITICAL" for v in vector_findings) else ("HIGH" if any(v["severity"] == "HIGH" for v in vector_findings) else "MEDIUM")
            risk_score = RiskEngine.calculate_test_risk(highest_sev, "Business Logic", False)
            severity = highest_sev
            status = "FAILED"

        # Record Test Run & Result in Database
        run_number = f"CUSTOM-{datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
        test_run = TestRun(
            run_number=run_number,
            execution_type="CUSTOM_USER_TEST",
            total_tests=1,
            passed=1 if is_overall_pass else 0,
            failed=0 if is_overall_pass else 1,
            critical_count=1 if severity == "CRITICAL" else 0,
            high_count=1 if severity == "HIGH" else 0,
            overall_risk_score=risk_score,
            security_score=round(100.0 - risk_score, 1),
            status="COMPLETED",
            executed_by=executed_by,
            started_at=datetime.datetime.utcnow(),
            completed_at=datetime.datetime.utcnow()
        )
        db.add(test_run)
        db.commit()
        db.refresh(test_run)

        evidence = {
            "api_name": api_name,
            "api_url": api_url,
            "method": method,
            "expected_status": expected_status,
            "actual_status": actual_status,
            "response_time_ms": response_time_ms,
            "headers_sent": req_headers,
            "payload_sent": payload,
            "response_snippet": response_text[:500],
            "vector_findings": vector_findings,
            "error_detail": error_detail
        }

        test_result = TestResult(
            test_run_id=test_run.id,
            test_case_id=f"CUSTOM-{uuid.uuid4().hex[:6].upper()}",
            test_name=f"Custom Test: {api_name}",
            category="Custom Security Vector",
            api_endpoint=api_url,
            status=status,
            severity=severity,
            risk_score=risk_score,
            actual_status=actual_status,
            evidence=evidence,
            recommendation=vector_findings[0]["recommendation"] if vector_findings else "Enforce strict security validation."
        )
        db.add(test_result)

        # Auto-generate Finding and Threat Flag if FAILED
        if status == "FAILED":
            finding_code = f"FIND-{uuid.uuid4().hex[:6].upper()}"
            db.add(Finding(
                finding_code=finding_code,
                title=f"Custom API Flaw: {api_name}",
                category="Custom API Testing",
                severity=severity,
                risk_score=risk_score,
                api_endpoint=api_url,
                status="OPEN",
                evidence=evidence,
                recommendation=test_result.recommendation
            ))

            flag_code = f"FLG-{uuid.uuid4().hex[:6].upper()}"
            db.add(ThreatFlag(
                flag_code=flag_code,
                title=f"Threat Flag: {api_name}",
                api_endpoint=api_url,
                category="Custom API Testing",
                severity=severity,
                risk_score=risk_score,
                status="OPEN",
                evidence_summary=f"User-executed test against {api_url} failed assertion (HTTP {actual_status}).",
                recommendation=test_result.recommendation
            ))

        # Audit Log
        db.add(AuditLog(
            user_email=executed_by,
            action="EXECUTE_CUSTOM_API_TEST",
            resource=api_url,
            result=status,
            risk_score=risk_score,
            details=evidence
        ))
        db.commit()

        return {
            "test_run_id": test_run.id,
            "run_number": run_number,
            "api_name": api_name,
            "api_url": api_url,
            "method": method,
            "status": status,
            "severity": severity,
            "risk_score": risk_score,
            "security_score": round(100.0 - risk_score, 1),
            "actual_status": actual_status,
            "response_time_ms": response_time_ms,
            "response_snippet": response_text[:500],
            "evidence": evidence,
            "vector_findings": vector_findings
        }

    @staticmethod
    def _generate_finding_and_flag(db: Session, tc: TestCase, evidence: dict, risk_score: float, recommendation: str):
        # Finding
        finding_code = f"FIND-{uuid.uuid4().hex[:6].upper()}"
        finding = Finding(
            finding_code=finding_code,
            title=f"Vulnerability in {tc.endpoint}: {tc.name}",
            category=tc.category,
            severity=tc.severity,
            risk_score=risk_score,
            api_endpoint=tc.endpoint,
            status="OPEN",
            evidence=evidence,
            recommendation=recommendation,
            cvss_score=8.5 if tc.severity == "CRITICAL" else (7.0 if tc.severity == "HIGH" else 4.5)
        )
        db.add(finding)

        # Flag
        flag_code = f"FLG-{uuid.uuid4().hex[:6].upper()}"
        flag = ThreatFlag(
            flag_code=flag_code,
            title=f"Security Threat: {tc.name}",
            api_endpoint=tc.endpoint,
            category=tc.category,
            severity=tc.severity,
            risk_score=risk_score,
            status="OPEN",
            evidence_summary=f"Endpoint {tc.endpoint} failed security assertion under test {tc.test_id}.",
            recommendation=recommendation
        )
        db.add(flag)

