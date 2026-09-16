from sqlalchemy.orm import Session
import datetime
import uuid
from app.models import SecurityIncident, MockTransaction, LoginAttempt, SecurityAlert, AuditLog

class MultiEventCorrelationEngine:
    @staticmethod
    def check_and_correlate(db: Session, account_number: str, current_tx: MockTransaction = None) -> SecurityIncident:
        # Check last 10 minutes events for this account
        window_start = datetime.datetime.utcnow() - datetime.timedelta(minutes=10)

        # 1. Fetch recent transactions
        recent_txs = db.query(MockTransaction).filter(
            MockTransaction.sender_account == account_number,
            MockTransaction.timestamp >= window_start
        ).order_by(MockTransaction.id.asc()).all()

        # 2. Fetch recent failed logins
        username = f"user_{account_number[-4:]}"
        failed_logins = db.query(LoginAttempt).filter(
            LoginAttempt.username == username,
            LoginAttempt.status == "FAILED",
            LoginAttempt.timestamp >= window_start
        ).all()

        # 3. Check suspicious indicators count
        high_risk_txs = [tx for tx in recent_txs if tx.risk_score >= 60.0]
        distinct_devices = set(tx.device_id for tx in recent_txs if tx.device_id)
        distinct_ips = set(tx.ip_address for tx in recent_txs if tx.ip_address)

        total_tx_count = len(recent_txs)
        failed_login_count = len(failed_logins)

        # Trigger correlation if >=2 distinct suspicious indicators occur together
        has_correlation = (
            (failed_login_count >= 2 and total_tx_count >= 1) or
            (len(distinct_devices) > 1 and total_tx_count >= 2) or
            (len(distinct_ips) > 1 and len(high_risk_txs) >= 1) or
            (total_tx_count >= 3 and len(high_risk_txs) >= 2)
        )

        if not has_correlation:
            return None

        # Build correlated incident details
        inc_code = f"INC-{uuid.uuid4().hex[:6].upper()}"
        events = []
        indicators = []

        if failed_login_count > 0:
            events.append(f"{failed_login_count} Failed Authentication Attempt(s)")
            indicators.append("FAILED_AUTH_SURGE")

        if len(distinct_devices) > 1:
            events.append(f"Unrecognized Device ID Switch ({list(distinct_devices)})")
            indicators.append("DEVICE_SWITCH")

        if len(distinct_ips) > 1:
            events.append(f"IP Location/Metadata Changed ({list(distinct_ips)})")
            indicators.append("IP_METADATA_SHIFT")

        if total_tx_count >= 3:
            events.append(f"{total_tx_count} Rapid Sequential Transfers")
            indicators.append("RAPID_TRANSACTIONS")

        if high_risk_txs:
            max_amt = max(tx.amount for tx in high_risk_txs)
            events.append(f"High-Risk Transfer Detected (₹{max_amt:,.2f})")
            indicators.append("HIGH_RISK_AMOUNT")

        tx_ids = [tx.transaction_id for tx in recent_txs]
        combined_score = min(100.0, 75.0 + (len(indicators) * 5.0))

        timeline = [
            {
                "timestamp": datetime.datetime.utcnow().strftime("%H:%M:%S"),
                "event": f"Correlated {len(indicators)} security anomalies across account {account_number}"
            }
        ]

        incident = SecurityIncident(
            incident_code=inc_code,
            title=f"Correlated Suspicious Activity — Account {account_number}",
            account_number=account_number,
            risk_score=combined_score,
            severity="CRITICAL" if combined_score >= 80.0 else "HIGH",
            status="OPEN",
            events_json=events,
            related_transactions=tx_ids,
            related_apis=["/api/v1/mock-bank/transfer", "/api/v1/auth/login"],
            security_indicators=indicators,
            timeline=timeline,
            recommended_action="Temporarily freeze high-value outbound API transfers and require secondary multi-factor authentication (MFA)."
        )

        db.add(incident)

        # Generate correlated alert as well
        alert = SecurityAlert(
            alert_code=f"ALT-{uuid.uuid4().hex[:6].upper()}",
            title=f"Correlated Security Incident [{inc_code}] Triggered",
            severity=incident.severity,
            endpoint="/mock-bank/transfer",
            transaction_id=current_tx.transaction_id if current_tx else (tx_ids[0] if tx_ids else None),
            message=f"Incident {inc_code} generated for account {account_number}: {', '.join(events)}.",
            status="ACTIVE",
            risk_score=incident.risk_score
        )
        db.add(alert)

        # Audit log entry
        audit = AuditLog(
            user_email="security_engine@system",
            action="INCIDENT_CREATED",
            resource=f"INCIDENT-{inc_code}",
            result="SUCCESS",
            risk_score=combined_score,
            details={"account": account_number, "events": events, "indicators": indicators}
        )
        db.add(audit)
        db.commit()
        db.refresh(incident)

        return incident
