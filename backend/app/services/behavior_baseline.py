from sqlalchemy.orm import Session
import datetime
from app.models import BehaviorProfile

class BehaviorBaselineService:
    @staticmethod
    def get_or_create_profile(db: Session, account_number: str) -> BehaviorProfile:
        profile = db.query(BehaviorProfile).filter(BehaviorProfile.account_number == account_number).first()
        if not profile:
            profile = BehaviorProfile(
                account_number=account_number,
                username=f"user_{account_number[-4:]}",
                avg_amount=7500.0,
                normal_min_amount=1000.0,
                normal_max_amount=25000.0,
                max_normal_transaction=50000.0,
                avg_daily_frequency=3.0,
                normal_start_hour=8,
                normal_end_hour=22,
                known_devices=["DEVICE-001"],
                known_ips=["192.168.1.50"],
                previous_security_events_count=0
            )
            db.add(profile)
            db.commit()
            db.refresh(profile)
        return profile

    @staticmethod
    def evaluate_transaction_against_baseline(db: Session, account_number: str, amount: float, device_id: str, ip_address: str, txn_time: datetime.datetime = None) -> list:
        if not txn_time:
            txn_time = datetime.datetime.utcnow()

        profile = BehaviorBaselineService.get_or_create_profile(db, account_number)
        indicators = []

        # 1. Amount Threshold Check (3x average or > normal max)
        if amount > (profile.avg_amount * 3.0) or amount > profile.normal_max_amount:
            multiplier = round(amount / profile.avg_amount, 1) if profile.avg_amount > 0 else 3.0
            indicators.append({
                "code": "IND-AMT-UNUSUAL",
                "name": "Unusual Transaction Amount",
                "severity": "HIGH" if amount > profile.max_normal_transaction else "MEDIUM",
                "points": 25.0 if amount > profile.max_normal_transaction else 20.0,
                "explanation": f"Transaction amount (₹{amount:,.2f}) is {multiplier}x historical average (₹{profile.avg_amount:,.2f}) and exceeds normal max (₹{profile.normal_max_amount:,.2f})."
            })

        # 2. Unknown / New Device Check
        known_devices = profile.known_devices or ["DEVICE-001"]
        if device_id not in known_devices:
            indicators.append({
                "code": "IND-DEV-NEW",
                "name": "New Unrecognized Device",
                "severity": "HIGH",
                "points": 15.0,
                "explanation": f"Transaction originated from unrecognized Device ID '{device_id}'. Known devices: {known_devices}."
            })

        # 3. Synthetic IP Metadata Change Check
        known_ips = profile.known_ips or ["192.168.1.50"]
        if ip_address not in known_ips:
            indicators.append({
                "code": "IND-IP-CHANGE",
                "name": "Synthetic IP Metadata Change",
                "severity": "MEDIUM",
                "points": 10.0,
                "explanation": f"IP address '{ip_address}' differs from user baseline primary IP address '{known_ips[0]}'."
            })

        # 4. Unusual Operating Hours Check
        current_hour = txn_time.hour
        if current_hour < profile.normal_start_hour or current_hour >= profile.normal_end_hour:
            indicators.append({
                "code": "IND-TIME-UNUSUAL",
                "name": "Unusual Transaction Time",
                "severity": "LOW",
                "points": 10.0,
                "explanation": f"Transaction executed at {txn_time.strftime('%H:%M:%S')}, outside user normal operating window ({profile.normal_start_hour:02d}:00–{profile.normal_end_hour:02d}:00)."
            })

        return indicators
