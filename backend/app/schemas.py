from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# --- Auth Schemas ---
class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    username: str

class LoginSchema(BaseModel):
    username: str
    password: str

class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str
    role: str = "TESTER"

class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

# --- API Target Schemas ---
class ApiTargetCreateSchema(BaseModel):
    name: str
    endpoint: str
    method: str
    description: Optional[str] = None
    environment: Optional[str] = "STAGING"
    auth_type: Optional[str] = "BEARER_JWT"
    expected_status_code: Optional[int] = 200
    headers: Optional[Dict[str, Any]] = {}
    body: Optional[Dict[str, Any]] = {}
    parameters: Optional[Dict[str, Any]] = {}
    required_fields: Optional[List[str]] = []
    expected_schema: Optional[Dict[str, Any]] = {}

class ApiTargetResponseSchema(ApiTargetCreateSchema):
    id: int
    risk_score: float
    risk_level: str
    created_at: datetime

    class Config:
        from_attributes = True

class CustomApiTestRequestSchema(BaseModel):
    api_name: Optional[str] = "Custom API Target"
    api_url: str
    method: str = "GET"
    auth_type: Optional[str] = "NONE"
    auth_token: Optional[str] = None
    headers: Optional[Dict[str, Any]] = {}
    parameters: Optional[Dict[str, Any]] = {}
    payload: Optional[Dict[str, Any]] = {}
    expected_status: Optional[int] = 200

# --- Test Schemas ---
class TestCaseResponseSchema(BaseModel):
    id: int
    test_id: str
    name: str
    category: str
    description: Optional[str]
    precondition: Optional[str]
    request_method: str
    endpoint: str
    expected_status: int
    expected_result: str
    severity: str
    vulnerability_toggle_key: Optional[str]

    class Config:
        from_attributes = True

class TestRunRequestSchema(BaseModel):
    execution_type: str = "FULL_SUITE"  # FULL_SUITE, SINGLE_API, REGRESSION
    api_endpoint: Optional[str] = None
    categories: Optional[List[str]] = []

class TestResultSchema(BaseModel):
    id: int
    test_case_id: str
    test_name: str
    category: str
    api_endpoint: str
    status: str
    severity: str
    risk_score: float
    actual_status: Optional[int]
    evidence: Dict[str, Any]
    recommendation: Optional[str]
    executed_at: datetime

    class Config:
        from_attributes = True

class TestRunResponseSchema(BaseModel):
    id: int
    run_number: str
    execution_type: str
    total_tests: int
    passed: int
    failed: int
    critical_count: int
    high_count: int
    overall_risk_score: float
    security_score: float
    status: str
    executed_by: str
    started_at: datetime
    completed_at: datetime
    results: List[TestResultSchema] = []

    class Config:
        from_attributes = True

# --- Finding & Threat Flag Schemas ---
class FindingResponseSchema(BaseModel):
    id: int
    finding_code: str
    title: str
    category: str
    severity: str
    risk_score: float
    api_endpoint: str
    status: str
    evidence: Dict[str, Any]
    recommendation: Optional[str]
    cvss_score: float
    created_at: datetime

    class Config:
        from_attributes = True

class FindingUpdateSchema(BaseModel):
    status: str
    analyst_notes: Optional[str] = None

class ThreatFlagResponseSchema(BaseModel):
    id: int
    flag_code: str
    title: str
    api_endpoint: str
    category: str
    severity: str
    risk_score: float
    status: str
    evidence_summary: Optional[str]
    recommendation: Optional[str]
    analyst_notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class ThreatFlagUpdateSchema(BaseModel):
    status: str
    analyst_notes: Optional[str] = None

# --- Mock Sandbox Schemas ---
class SandboxToggleSchema(BaseModel):
    id: int
    key: str
    name: str
    category: str
    description: str
    is_enabled: bool

    class Config:
        from_attributes = True

class SandboxToggleUpdateSchema(BaseModel):
    key: str
    is_enabled: bool

class MockTransferSchema(BaseModel):
    sender_account: str
    receiver_account: str
    amount: float
    currency: Optional[str] = "INR"
    device_id: Optional[str] = "DEVICE-001"
    ip_address: Optional[str] = "192.168.1.50"

class FalsePositiveUpdateSchema(BaseModel):
    is_false_positive: bool
    tester_name: str
    reason: str

class IncidentUpdateSchema(BaseModel):
    status: str  # OPEN, INVESTIGATING, RESOLVED, FALSE_POSITIVE
    resolution_notes: Optional[str] = None
    marked_by: Optional[str] = None

class RiskRuleUpdateSchema(BaseModel):
    rule_key: str
    is_enabled: Optional[bool] = True
    weight: Optional[float] = 15.0
    params: Optional[Dict[str, Any]] = None

class BankingRuleUpdateSchema(BaseModel):
    rule_code: str
    is_enabled: Optional[bool] = True
    threshold_value: Optional[float] = 0.0
    action_on_fail: Optional[str] = "REJECT"
    risk_weight: Optional[float] = 25.0

class ScenarioRunRequestSchema(BaseModel):
    scenario_key: str  # NORMAL, HIGH_AMOUNT, RAPID_TXNS, NEW_DEVICE, IP_CHANGE, FAILED_LOGIN_TRANSFER, DUPLICATE_TXN, LIMIT_VIOLATION, COMBINED_SUSPICIOUS
    sender_account: Optional[str] = "ACC-1001"
    receiver_account: Optional[str] = "ACC-1002"

class SelectedTestsRunRequestSchema(BaseModel):
    modules: List[str]  # Authentication, Authorization, Functional, Negative, Security, Banking Rules, Transaction Monitoring, Performance

class OpenApiImportSchema(BaseModel):
    title: str
    version: str
    endpoints_json: List[Dict[str, Any]]

# --- Dashboard & Report Schemas ---
class DashboardSummarySchema(BaseModel):
    total_apis: int
    tests_executed: int
    tests_passed: int
    tests_failed: int
    critical_findings: int
    high_findings: int
    active_flags: int
    overall_risk_score: float
    security_score: float
    api_health: Dict[str, float]
    risk_distribution: Dict[str, int]
    recent_alerts: List[Dict[str, Any]]

class SecurityReportCreateSchema(BaseModel):
    title: str
    format: str = "PDF"

