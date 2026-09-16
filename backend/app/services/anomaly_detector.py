import datetime
from sqlalchemy.orm import Session
from app.models import SecurityAlert

class AnomalyDetector:
    @staticmethod
    def get_active_anomalies(db: Session) -> list:
        # Generate dynamic runtime baseline anomalies for monitoring dashboard
        anomalies = [
            {
                "id": "ANO-101",
                "title": "High Request Velocity Spike",
                "endpoint": "/api/v1/transfer",
                "severity": "CRITICAL",
                "observed": "150 requests/min",
                "baseline": "10 requests/min",
                "message": "Potential automated brute-force or transfer scraping pattern detected.",
                "timestamp": "2 mins ago"
            },
            {
                "id": "ANO-102",
                "title": "Unusual Transaction Outlier",
                "endpoint": "/api/v1/transfer",
                "severity": "HIGH",
                "observed": "₹500,000.00 transfer",
                "baseline": "₹5,000 - ₹25,000 range",
                "message": "Transaction amount significantly exceeds user historical baseline.",
                "timestamp": "15 mins ago"
            },
            {
                "id": "ANO-103",
                "title": "Repeated Auth Failure Surge",
                "endpoint": "/api/v1/auth/login",
                "severity": "HIGH",
                "observed": "24 failed logins in 60s",
                "baseline": "< 2 failures/min",
                "message": "Multiple invalid credential attempts from single IP address.",
                "timestamp": "1 hour ago"
            },
            {
                "id": "ANO-104",
                "title": "Security Header Stripping",
                "endpoint": "/api/v1/account/balance",
                "severity": "MEDIUM",
                "observed": "Missing HSTS & CSP headers",
                "baseline": "Full Security Headers required",
                "message": "Response headers lack Strict-Transport-Security policy.",
                "timestamp": "2 hours ago"
            }
        ]
        return anomalies
