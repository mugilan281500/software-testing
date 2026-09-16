from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models import (
    User, ApiTarget, TestCase, MockAccount, MockBeneficiary, MockSandboxToggle, AuditLog,
    BankingRule, RiskRule, BehaviorProfile
)
from app.auth_utils import get_password_hash
from app.services.test_orchestrator import TestOrchestratorService

def seed_database():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # 1. Seed Users
        if db.query(User).count() == 0:
            users = [
                User(username="admin", email="admin@banksecure.io", hashed_password=get_password_hash("admin123"), role="ADMIN"),
                User(username="analyst", email="analyst@banksecure.io", hashed_password=get_password_hash("analyst123"), role="SECURITY_ANALYST"),
                User(username="tester", email="tester@banksecure.io", hashed_password=get_password_hash("tester123"), role="TESTER"),
                User(username="customer", email="customer@banksecure.io", hashed_password=get_password_hash("customer123"), role="CUSTOMER"),
            ]
            db.add_all(users)
            db.commit()

        # 2. Seed Mock Banking Accounts
        if db.query(MockAccount).count() == 0:
            accounts = [
                MockAccount(account_number="ACC-1001", owner_name="Mukilan M (Primary Customer)", email="usera@bank.com", balance=75000.0, role="USER", daily_limit=100000.0),
                MockAccount(account_number="ACC-1002", owner_name="Jane Doe (Beneficiary User)", email="userb@bank.com", balance=35000.0, role="USER", daily_limit=100000.0),
                MockAccount(account_number="ACC-1003", owner_name="Corporate Payroll Pool", email="corporate@bank.com", balance=500000.0, role="ADMIN", daily_limit=1000000.0),
            ]
            db.add_all(accounts)
            db.commit()

        # Seed Beneficiaries
        if db.query(MockBeneficiary).count() == 0:
            bens = [
                MockBeneficiary(account_number="ACC-1001", beneficiary_account="ACC-1002", beneficiary_name="Jane Doe", bank_name="BankSecure"),
                MockBeneficiary(account_number="ACC-1001", beneficiary_account="ACC-1003", beneficiary_name="Corporate Payroll Pool", bank_name="BankSecure")
            ]
            db.add_all(bens)
            db.commit()

        # 3. Seed Behavior Profiles
        if db.query(BehaviorProfile).count() == 0:
            profiles = [
                BehaviorProfile(
                    account_number="ACC-1001",
                    username="user_1001",
                    avg_amount=5000.0,
                    normal_min_amount=1000.0,
                    normal_max_amount=25000.0,
                    max_normal_transaction=50000.0,
                    avg_daily_frequency=3.0,
                    normal_start_hour=8,
                    normal_end_hour=22,
                    known_devices=["DEVICE-001"],
                    known_ips=["192.168.1.50"]
                ),
                BehaviorProfile(
                    account_number="ACC-1002",
                    username="user_1002",
                    avg_amount=3000.0,
                    normal_min_amount=500.0,
                    normal_max_amount=15000.0,
                    max_normal_transaction=30000.0,
                    avg_daily_frequency=2.0,
                    normal_start_hour=8,
                    normal_end_hour=22,
                    known_devices=["DEVICE-002"],
                    known_ips=["10.0.0.15"]
                )
            ]
            db.add_all(profiles)
            db.commit()

        # 4. Seed Banking Business Rules
        if db.query(BankingRule).count() == 0:
            b_rules = [
                BankingRule(rule_code="RULE-ACCOUNT-STATUS", name="Account Active & Unblocked Status", description="Sender account must be active and not blocked or frozen", rule_type="STATUS", is_enabled=True, action_on_fail="REJECT", risk_weight=30.0),
                BankingRule(rule_code="RULE-AMOUNT-BOUNDS", name="Transaction Amount Bounds Check", description="Transaction amount must be strictly greater than zero", rule_type="VALIDATION", is_enabled=True, action_on_fail="REJECT", risk_weight=35.0),
                BankingRule(rule_code="RULE-BALANCE-CHECK", name="Sufficient Account Balance Check", description="Sender account balance must cover the requested transfer amount", rule_type="BALANCE", is_enabled=True, action_on_fail="REJECT", risk_weight=25.0),
                BankingRule(rule_code="RULE-MIN-BALANCE", name="Minimum Account Threshold Maintenance", description="Account balance must remain above minimum required balance (₹1,000)", rule_type="BALANCE", is_enabled=True, threshold_value=1000.0, action_on_fail="INCREMENT_RISK", risk_weight=15.0),
                BankingRule(rule_code="RULE-DAILY-LIMIT", name="Cumulative Daily Transfer Limit", description="Total daily transfer amount must not exceed daily limit (₹100,000)", rule_type="LIMIT", is_enabled=True, threshold_value=100000.0, action_on_fail="MONITOR", risk_weight=20.0),
                BankingRule(rule_code="RULE-BENEFICIARY", name="Verified Beneficiary Account Check", description="Recipient account must be in sender verified beneficiary directory", rule_type="VERIFICATION", is_enabled=True, action_on_fail="INCREMENT_RISK", risk_weight=15.0),
                BankingRule(rule_code="RULE-CURRENCY", name="Supported Currency Validation", description="Transaction currency must be in approved ISO list (INR, USD, EUR)", rule_type="CURRENCY", is_enabled=True, action_on_fail="REJECT", risk_weight=10.0),
                BankingRule(rule_code="RULE-DUPLICATE-TX", name="Recent Duplicate Transaction Check", description="Identical transfers within 2 minutes generate warning flag", rule_type="DUPLICATE", is_enabled=True, action_on_fail="INCREMENT_RISK", risk_weight=25.0),
            ]
            db.add_all(b_rules)
            db.commit()

        # 5. Seed Risk Rules
        if db.query(RiskRule).count() == 0:
            r_rules = [
                RiskRule(rule_key="UNUSUAL_AMOUNT_THRESHOLD", category="BEHAVIOR", name="Unusual Amount Multiplier", description="Flag amount >3x average historical baseline", weight=20.0, is_enabled=True, params={"multiplier": 3.0}),
                RiskRule(rule_key="RAPID_TXN_WINDOW", category="FREQUENCY", name="Rapid Transaction Window", description="Flag >3 transactions executed within 2 minutes", weight=20.0, is_enabled=True, params={"window_minutes": 2, "max_txns": 3}),
                RiskRule(rule_key="NEW_DEVICE_FLAG", category="DEVICE", name="New Device Detection", description="Flag unrecognized device ID", weight=15.0, is_enabled=True, params={}),
                RiskRule(rule_key="IP_CHANGE_FLAG", category="NETWORK", name="IP Metadata Shift", description="Flag change in synthetic client IP address", weight=10.0, is_enabled=True, params={}),
                RiskRule(rule_key="FAILED_LOGIN_FLAG", category="AUTHENTICATION", name="Recent Failed Login Spike", description="Flag >2 failed login attempts within 15 minutes", weight=15.0, is_enabled=True, params={"window_minutes": 15, "max_fails": 2}),
                RiskRule(rule_key="HIGH_RISK_BOUND", category="THRESHOLD", name="HIGH Risk Level Threshold", description="Score boundary for HIGH risk level classification", weight=60.0, is_enabled=True, params={"threshold": 60.0}),
                RiskRule(rule_key="CRITICAL_RISK_BOUND", category="THRESHOLD", name="CRITICAL Risk Level Threshold", description="Score boundary for CRITICAL risk level classification", weight=80.0, is_enabled=True, params={"threshold": 80.0}),
            ]
            db.add_all(r_rules)
            db.commit()

        # 6. Seed Mock Sandbox Vulnerability Toggles
        if db.query(MockSandboxToggle).count() == 0:
            toggles = [
                MockSandboxToggle(key="VULN_EXPIRED_JWT", name="Accept Expired / Modified JWT", category="Authentication", description="Simulates API accepting invalid or expired Bearer tokens.", is_enabled=True),
                MockSandboxToggle(key="VULN_IDOR_CROSS_ACCOUNT", name="Broken Access Control (IDOR)", category="Authorization", description="Simulates User A reading or transferring from User B account.", is_enabled=True),
                MockSandboxToggle(key="VULN_NEGATIVE_TRANSFER", name="Allow Negative Transaction Amounts", category="Business Logic", description="Simulates server accepting negative transfer values (-₹5000).", is_enabled=True),
                MockSandboxToggle(key="VULN_INSUFFICIENT_BALANCE", name="Allow Overdraft / Insufficient Balance", category="Business Logic", description="Simulates transferring funds beyond available account balance.", is_enabled=False),
                MockSandboxToggle(key="VULN_RATE_LIMIT_BYPASS", name="Rate Limit Bypass / Weak Throttling", category="Rate Limiting", description="Allows unlimited requests without returning 429 Too Many Requests.", is_enabled=True),
                MockSandboxToggle(key="VULN_MISSING_HEADERS", name="Missing Security Headers", category="Security Headers", description="Omits Strict-Transport-Security, CSP, and X-Frame-Options.", is_enabled=True),
                MockSandboxToggle(key="VULN_DATA_LEAKAGE", name="Expose Sensitive Database Stack Trace", category="Data Protection", description="Returns DB passwords or stack traces in error responses.", is_enabled=False),
            ]
            db.add_all(toggles)
            db.commit()

        # 7. Seed API Targets
        if db.query(ApiTarget).count() == 0:
            apis = [
                ApiTarget(name="Fund Transfer API", endpoint="/mock-bank/transfer", method="POST", description="Processes peer-to-peer and interbank fund transfers", environment="STAGING", auth_type="BEARER_JWT", expected_status_code=200, risk_score=87.5, risk_level="CRITICAL", regression_priority="CRITICAL"),
                ApiTarget(name="Account Balance API", endpoint="/mock-bank/accounts", method="GET", description="Returns balance details for specified account number", environment="STAGING", auth_type="BEARER_JWT", expected_status_code=200, risk_score=32.0, risk_level="MEDIUM", regression_priority="NORMAL"),
                ApiTarget(name="User Auth Login API", endpoint="/auth/login", method="POST", description="Authenticates customer credentials and issues JWT token", environment="STAGING", auth_type="NONE", expected_status_code=200, risk_score=18.0, risk_level="LOW", regression_priority="NORMAL"),
                ApiTarget(name="Payment Gateway API", endpoint="/mock-bank/payment", method="POST", description="Executes merchant card and UPI payments", environment="STAGING", auth_type="BEARER_JWT", expected_status_code=200, risk_score=82.0, risk_level="HIGH", regression_priority="HIGH"),
                ApiTarget(name="Beneficiary Management API", endpoint="/mock-bank/beneficiary", method="POST", description="Adds new transfer recipient account details", environment="STAGING", auth_type="BEARER_JWT", expected_status_code=200, risk_score=65.0, risk_level="HIGH", regression_priority="NORMAL"),
                ApiTarget(name="Admin User Directory API", endpoint="/admin/users", method="GET", description="Lists enterprise user directory for admin role", environment="STAGING", auth_type="BEARER_JWT", expected_status_code=200, risk_score=91.0, risk_level="CRITICAL", regression_priority="CRITICAL"),
            ]
            db.add_all(apis)
            db.commit()

        # 8. Seed Test Cases
        if db.query(TestCase).count() == 0:
            test_cases = [
                # Authentication Tests
                TestCase(test_id="AUTH-001", name="Valid Username & Password Login", category="Authentication", description="Validates standard login flow returns JWT", precondition="User exists", request_method="POST", endpoint="/auth/login", expected_status=200, expected_result="Returns HTTP 200 with JWT token", severity="LOW"),
                TestCase(test_id="AUTH-002", name="Expired JWT Token Access", category="Authentication", description="Tests whether expired tokens are rejected", precondition="Expired JWT token", request_method="GET", endpoint="/mock-bank/accounts", expected_status=401, expected_result="Returns HTTP 401 Unauthorized", severity="HIGH", vulnerability_toggle_key="VULN_EXPIRED_JWT"),
                TestCase(test_id="AUTH-003", name="Missing Bearer Authorization Header", category="Authentication", description="Sends request without Authorization header", precondition="None", request_method="GET", endpoint="/mock-bank/accounts", expected_status=401, expected_result="Returns HTTP 401 Unauthorized", severity="HIGH"),
                
                # Authorization Tests
                TestCase(test_id="AUTHZ-001", name="User A Accessing User B Account (IDOR)", category="Authorization", description="Tests cross-user account access attempt", precondition="User A token", request_method="GET", endpoint="/mock-bank/accounts", expected_status=403, expected_result="Returns HTTP 403 Forbidden", severity="CRITICAL", vulnerability_toggle_key="VULN_IDOR_CROSS_ACCOUNT"),
                TestCase(test_id="AUTHZ-002", name="Standard User Accessing Admin API", category="Authorization", description="Vertical privilege escalation test", precondition="User token", request_method="GET", endpoint="/admin/users", expected_status=403, expected_result="Returns HTTP 403 Forbidden", severity="CRITICAL"),
                
                # Functional / Banking Rules Tests
                TestCase(test_id="LOGIC-001", name="Negative Fund Transfer Attempt (-₹5,000)", category="Banking Rules", description="Tests negative transfer input processing", precondition="Valid token", request_method="POST", endpoint="/mock-bank/transfer", expected_status=400, expected_result="Returns HTTP 400 Bad Request", severity="CRITICAL", vulnerability_toggle_key="VULN_NEGATIVE_TRANSFER"),
                TestCase(test_id="LOGIC-002", name="Insufficient Balance Transfer Attempt", category="Banking Rules", description="Transfer amount exceeding account balance", precondition="Account balance ₹75,000", request_method="POST", endpoint="/mock-bank/transfer", expected_status=400, expected_result="Returns HTTP 400 Bad Request", severity="HIGH", vulnerability_toggle_key="VULN_INSUFFICIENT_BALANCE"),
                TestCase(test_id="LOGIC-003", name="Zero Amount Fund Transfer (₹0)", category="Banking Rules", description="Transfer zero value request", precondition="Valid token", request_method="POST", endpoint="/mock-bank/transfer", expected_status=400, expected_result="Returns HTTP 400 Bad Request", severity="MEDIUM"),
                
                # Negative Tests
                TestCase(test_id="NEG-001", name="String Payload in Amount Field", category="Negative", description="Passes string instead of float for transfer amount", precondition="None", request_method="POST", endpoint="/mock-bank/transfer", expected_status=422, expected_result="Returns HTTP 422 Unprocessable Entity", severity="MEDIUM"),

                # Rate Limiting Tests
                TestCase(test_id="RATE-001", name="100 Rapid Requests Throttling Test", category="Performance", description="Burst 100 requests in 5 seconds to test HTTP 429", precondition="High concurrency", request_method="POST", endpoint="/mock-bank/transfer", expected_status=429, expected_result="Returns HTTP 429 Too Many Requests", severity="HIGH", vulnerability_toggle_key="VULN_RATE_LIMIT_BYPASS"),

                # Security Tests
                TestCase(test_id="SEC-001", name="Strict-Transport-Security (HSTS) Header", category="Security", description="Verifies HSTS header is present in API response", precondition="None", request_method="GET", endpoint="/mock-bank/accounts", expected_status=200, expected_result="Response contains Strict-Transport-Security", severity="MEDIUM", vulnerability_toggle_key="VULN_MISSING_HEADERS"),
            ]
            db.add_all(test_cases)
            db.commit()

        # 9. Initial Test Orchestration Execution
        if db.query(TestCase).count() > 0:
            TestOrchestratorService.execute_test_suite(db=db, trigger_source="INITIAL_SEED")

    finally:
        db.close()

if __name__ == "__main__":
    seed_database()

