import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="TESTER", nullable=False)  # ADMIN, SECURITY_ANALYST, TESTER, CUSTOMER
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MockAccount(Base):
    __tablename__ = "mock_accounts"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True, nullable=False)
    owner_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    balance = Column(Float, default=50000.0)
    role = Column(String, default="USER")  # USER, ADMIN
    daily_limit = Column(Float, default=100000.0)
    is_blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class MockBeneficiary(Base):
    __tablename__ = "mock_beneficiaries"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, nullable=False, index=True)  # Belongs to sender
    beneficiary_account = Column(String, nullable=False)
    beneficiary_name = Column(String, nullable=False)
    bank_name = Column(String, default="BankSecure")
    is_verified = Column(Boolean, default=True)

class MockTransaction(Base):
    __tablename__ = "mock_transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, unique=True, index=True, nullable=False)
    sender_account = Column(String, nullable=False, index=True)
    receiver_account = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")
    status = Column(String, default="COMPLETED")  # COMPLETED, MONITOR, REVIEW, BLOCKED, REJECTED
    type = Column(String, default="TRANSFER")
    device_id = Column(String, default="DEVICE-001")
    ip_address = Column(String, default="192.168.1.50")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

    risk_score = Column(Float, default=0.0)
    risk_level = Column(String, default="LOW")  # LOW, MEDIUM, HIGH, CRITICAL
    decision = Column(String, default="ALLOWED")  # ALLOWED, MONITOR, REVIEW, BLOCKED
    flags_count = Column(Integer, default=0)

    # Relationships
    security_events = relationship("TransactionSecurityEvent", back_populates="transaction", cascade="all, delete-orphan")
    risk_breakdown = relationship("TransactionRiskScore", back_populates="transaction", uselist=False, cascade="all, delete-orphan")

class TransactionSecurityEvent(Base):
    __tablename__ = "transaction_security_events"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, ForeignKey("mock_transactions.transaction_id"), nullable=False)
    indicator_code = Column(String, nullable=False)  # e.g., IND-AMT, IND-FREQ, IND-DEV, IND-IP
    indicator_name = Column(String, nullable=False)
    severity = Column(String, default="MEDIUM")
    score_impact = Column(Float, default=0.0)
    explanation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    transaction = relationship("MockTransaction", back_populates="security_events")

class TransactionRiskScore(Base):
    __tablename__ = "transaction_risk_scores"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String, ForeignKey("mock_transactions.transaction_id"), unique=True, nullable=False)
    overall_score = Column(Float, default=0.0)
    risk_level = Column(String, default="LOW")
    decision = Column(String, default="ALLOWED")
    
    # Category Breakdown Scores (0-100)
    auth_score = Column(Float, default=100.0)
    authz_score = Column(Float, default=100.0)
    validation_score = Column(Float, default=100.0)
    business_rules_score = Column(Float, default=100.0)
    behavior_score = Column(Float, default=100.0)
    api_security_score = Column(Float, default=100.0)

    factors_json = Column(JSON, default=list)  # list of factor dicts {factor, points, explanation}
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    transaction = relationship("MockTransaction", back_populates="risk_breakdown")

class BehaviorProfile(Base):
    __tablename__ = "behavior_profiles"

    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    avg_amount = Column(Float, default=5000.0)
    normal_min_amount = Column(Float, default=500.0)
    normal_max_amount = Column(Float, default=25000.0)
    max_normal_transaction = Column(Float, default=50000.0)
    avg_daily_frequency = Column(Float, default=3.0)
    normal_start_hour = Column(Integer, default=8)  # 08:00
    normal_end_hour = Column(Integer, default=22)   # 22:00
    known_devices = Column(JSON, default=lambda: ["DEVICE-001", "DEVICE-002"])
    known_ips = Column(JSON, default=lambda: ["192.168.1.50", "192.168.1.51"])
    previous_security_events_count = Column(Integer, default=0)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class DeviceSession(Base):
    __tablename__ = "device_sessions"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    device_id = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    user_agent = Column(String, default="Mozilla/5.0")
    is_trusted = Column(Boolean, default=True)
    last_active = Column(DateTime, default=datetime.datetime.utcnow)

class LoginAttempt(Base):
    __tablename__ = "login_attempts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, index=True)
    ip_address = Column(String, nullable=False)
    status = Column(String, nullable=False)  # SUCCESS, FAILED
    reason = Column(String, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class SecurityIncident(Base):
    __tablename__ = "security_incidents"

    id = Column(Integer, primary_key=True, index=True)
    incident_code = Column(String, unique=True, index=True, nullable=False)  # e.g., INC-001
    title = Column(String, nullable=False)
    account_number = Column(String, nullable=True)
    risk_score = Column(Float, default=0.0)
    severity = Column(String, default="HIGH")  # CRITICAL, HIGH, MEDIUM, LOW
    status = Column(String, default="OPEN")    # OPEN, INVESTIGATING, RESOLVED, FALSE_POSITIVE
    
    events_json = Column(JSON, default=list)            # List of correlated event summaries
    related_transactions = Column(JSON, default=list)  # List of transaction IDs
    related_apis = Column(JSON, default=list)          # List of API endpoints
    security_indicators = Column(JSON, default=list)   # Indicators detected
    timeline = Column(JSON, default=list)              # Chronological event log
    recommended_action = Column(Text, nullable=True)

    # Tester feedback / False Positive Management
    marked_by = Column(String, nullable=True)
    marked_at = Column(DateTime, nullable=True)
    resolution_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class SecurityAlert(Base):
    __tablename__ = "security_alerts"

    id = Column(Integer, primary_key=True, index=True)
    alert_code = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    severity = Column(String, default="HIGH")
    endpoint = Column(String, nullable=False)
    transaction_id = Column(String, nullable=True)
    message = Column(Text, nullable=False)
    status = Column(String, default="ACTIVE")  # ACTIVE, RESOLVED, DISMISSED
    risk_score = Column(Float, default=0.0)
    details = Column(JSON, default=dict)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class ApiTarget(Base):
    __tablename__ = "api_targets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    endpoint = Column(String, nullable=False, unique=True)
    method = Column(String, nullable=False)  # GET, POST, PUT, DELETE, etc.
    description = Column(Text, nullable=True)
    environment = Column(String, default="STAGING")
    auth_type = Column(String, default="BEARER_JWT")
    expected_status_code = Column(Integer, default=200)
    headers = Column(JSON, default=dict)
    body = Column(JSON, default=dict)
    parameters = Column(JSON, default=dict)
    required_fields = Column(JSON, default=list)
    expected_schema = Column(JSON, default=dict)
    risk_score = Column(Float, default=0.0)
    risk_level = Column(String, default="LOW")
    security_score = Column(Float, default=100.0)
    regression_priority = Column(String, default="NORMAL")  # NORMAL, HIGH, CRITICAL
    version = Column(String, default="v1.0.0")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True, index=True)
    test_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)  # Authentication, Authorization, Functional, Negative, Security, Banking Rules, Performance
    description = Column(Text, nullable=True)
    precondition = Column(Text, nullable=True)
    request_method = Column(String, default="GET")
    endpoint = Column(String, nullable=False)
    headers = Column(JSON, default=dict)
    body = Column(JSON, default=dict)
    expected_status = Column(Integer, nullable=False)
    expected_result = Column(Text, nullable=False)
    severity = Column(String, default="MEDIUM")
    status = Column(String, default="NOT_RUN")  # NOT_RUN, RUNNING, PASS, FAIL, WARNING, SKIPPED
    vulnerability_toggle_key = Column(String, nullable=True)

class TestRun(Base):
    __tablename__ = "test_runs"

    id = Column(Integer, primary_key=True, index=True)
    run_number = Column(String, unique=True, index=True, nullable=False)
    execution_type = Column(String, default="FULL_SUITE")  # FULL_SUITE, SELECTED, REGRESSION, AUTO_TRIGGERED
    total_tests = Column(Integer, default=0)
    passed = Column(Integer, default=0)
    failed = Column(Integer, default=0)
    warning_count = Column(Integer, default=0)
    critical_count = Column(Integer, default=0)
    high_count = Column(Integer, default=0)
    overall_risk_score = Column(Float, default=0.0)
    security_score = Column(Float, default=100.0)
    duration_ms = Column(Float, default=0.0)
    status = Column(String, default="COMPLETED")
    executed_by = Column(String, default="ADMIN")
    trigger_source = Column(String, default="MANUAL")  # MANUAL, AUTO_TRIGGER_HIGH_RISK
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, default=datetime.datetime.utcnow)

    results = relationship("TestResult", back_populates="test_run", cascade="all, delete-orphan")

class TestResult(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    test_run_id = Column(Integer, ForeignKey("test_runs.id"))
    test_case_id = Column(String, nullable=False)
    test_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    api_endpoint = Column(String, nullable=False)
    status = Column(String, nullable=False)  # PASS, FAIL, WARNING, SKIPPED
    severity = Column(String, default="LOW")
    risk_score = Column(Float, default=0.0)
    actual_status = Column(Integer, nullable=True)
    response_time_ms = Column(Float, default=0.0)
    evidence = Column(JSON, default=dict)       # expected vs actual response validation
    recommendation = Column(Text, nullable=True)
    executed_at = Column(DateTime, default=datetime.datetime.utcnow)

    test_run = relationship("TestRun", back_populates="results")

class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, index=True)
    finding_code = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    category = Column(String, nullable=False)
    severity = Column(String, default="MEDIUM")
    risk_score = Column(Float, default=0.0)
    api_endpoint = Column(String, nullable=False)
    status = Column(String, default="OPEN")  # OPEN, INVESTIGATING, RESOLVED, FALSE_POSITIVE, ACCEPTED_RISK
    evidence = Column(JSON, default=dict)
    recommendation = Column(Text, nullable=True)
    cvss_score = Column(Float, default=5.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class BankingRule(Base):
    __tablename__ = "banking_rules"

    id = Column(Integer, primary_key=True, index=True)
    rule_code = Column(String, unique=True, index=True, nullable=False)  # e.g., RULE-BAL, RULE-LIMIT
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    rule_type = Column(String, nullable=False)
    is_enabled = Column(Boolean, default=True)
    threshold_value = Column(Float, default=0.0)
    action_on_fail = Column(String, default="REJECT")  # REJECT, MONITOR, INCREMENT_RISK
    risk_weight = Column(Float, default=25.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class RiskRule(Base):
    __tablename__ = "risk_rules"

    id = Column(Integer, primary_key=True, index=True)
    rule_key = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    weight = Column(Float, default=15.0)
    is_enabled = Column(Boolean, default=True)
    params = Column(JSON, default=dict)  # threshold multipliers, time windows, counts

class ApiRiskScore(Base):
    __tablename__ = "api_risk_scores"

    id = Column(Integer, primary_key=True, index=True)
    endpoint = Column(String, unique=True, index=True, nullable=False)
    method = Column(String, default="POST")
    auth_score = Column(Float, default=95.0)
    authz_score = Column(Float, default=90.0)
    input_validation_score = Column(Float, default=85.0)
    rate_limiting_score = Column(Float, default=80.0)
    data_protection_score = Column(Float, default=95.0)
    overall_api_score = Column(Float, default=89.0)
    risk_level = Column(String, default="LOW")
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class ThreatFlag(Base):
    __tablename__ = "threat_flags"

    id = Column(Integer, primary_key=True, index=True)
    flag_code = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    api_endpoint = Column(String, nullable=False)
    category = Column(String, nullable=False)
    severity = Column(String, default="HIGH")
    risk_score = Column(Float, default=0.0)
    status = Column(String, default="OPEN")
    evidence_summary = Column(Text, nullable=True)
    recommendation = Column(Text, nullable=True)
    analyst_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, nullable=False)
    action = Column(String, nullable=False)  # LOGIN, FAILED_LOGIN, TRANSACTION_STARTED, TRANSACTION_COMPLETED, TRANSACTION_FLAGGED, SECURITY_TEST, RULE_CHANGED, ALERT_CREATED, REPORT_GENERATED
    resource = Column(String, nullable=False)
    result = Column(String, default="SUCCESS")
    risk_score = Column(Float, default=0.0)
    details = Column(JSON, default=dict)
    ip_address = Column(String, default="127.0.0.1")
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)

class MockSandboxToggle(Base):
    __tablename__ = "mock_sandbox_toggles"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    is_enabled = Column(Boolean, default=False)

class RiskHistory(Base):
    __tablename__ = "risk_history"

    id = Column(Integer, primary_key=True, index=True)
    overall_score = Column(Float, nullable=False)
    security_score = Column(Float, nullable=False)
    critical_flags = Column(Integer, default=0)
    high_flags = Column(Integer, default=0)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class SecurityReport(Base):
    __tablename__ = "security_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_code = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    format = Column(String, default="PDF")
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    risk_score = Column(Float, default=0.0)
    security_score = Column(Float, default=100.0)
    created_by = Column(String, default="ADMIN")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

