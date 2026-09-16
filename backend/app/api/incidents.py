from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import datetime
from app.database import get_db
from app.models import SecurityIncident, AuditLog
from app.schemas import FalsePositiveUpdateSchema, IncidentUpdateSchema

router = APIRouter(prefix="/incidents", tags=["Correlated Incident & False Positive Management"])

@router.get("")
def list_security_incidents(db: Session = Depends(get_db)):
    incidents = db.query(SecurityIncident).order_by(SecurityIncident.id.desc()).all()
    return incidents

@router.get("/{incident_code}")
def get_incident_details(incident_code: str, db: Session = Depends(get_db)):
    incident = db.query(SecurityIncident).filter(SecurityIncident.incident_code == incident_code).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return incident

@router.put("/{incident_code}/status")
def update_incident_status(incident_code: str, update_in: IncidentUpdateSchema, db: Session = Depends(get_db)):
    incident = db.query(SecurityIncident).filter(SecurityIncident.incident_code == incident_code).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    incident.status = update_in.status
    if update_in.resolution_notes:
        incident.resolution_notes = update_in.resolution_notes
    if update_in.marked_by:
        incident.marked_by = update_in.marked_by
    incident.marked_at = datetime.datetime.utcnow()

    # Append timeline entry
    timeline = incident.timeline or []
    timeline.append({
        "timestamp": datetime.datetime.utcnow().strftime("%H:%M:%S"),
        "event": f"Status changed to {update_in.status} by {update_in.marked_by or 'Tester'}"
    })
    incident.timeline = timeline

    # Audit Log
    audit = AuditLog(
        user_email=update_in.marked_by or "tester@banksecure.io",
        action="INCIDENT_STATUS_CHANGE",
        resource=f"INCIDENT-{incident_code}",
        result="SUCCESS",
        risk_score=incident.risk_score,
        details={"status": update_in.status, "notes": update_in.resolution_notes}
    )
    db.add(audit)
    db.commit()
    db.refresh(incident)

    return {"message": "Incident status updated successfully", "incident": incident}

@router.post("/{incident_code}/mark-false-positive")
def mark_false_positive(incident_code: str, payload: FalsePositiveUpdateSchema, db: Session = Depends(get_db)):
    incident = db.query(SecurityIncident).filter(SecurityIncident.incident_code == incident_code).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")

    new_status = "FALSE_POSITIVE" if payload.is_false_positive else "RESOLVED"
    incident.status = new_status
    incident.marked_by = payload.tester_name
    incident.marked_at = datetime.datetime.utcnow()
    incident.resolution_notes = payload.reason

    timeline = incident.timeline or []
    timeline.append({
        "timestamp": datetime.datetime.utcnow().strftime("%H:%M:%S"),
        "event": f"Marked as {new_status} by {payload.tester_name}. Reason: {payload.reason}"
    })
    incident.timeline = timeline

    audit = AuditLog(
        user_email=payload.tester_name,
        action="RULE_TUNING_FALSE_POSITIVE" if payload.is_false_positive else "INCIDENT_RESOLVED",
        resource=f"INCIDENT-{incident_code}",
        result="SUCCESS",
        risk_score=incident.risk_score,
        details={"tester": payload.tester_name, "reason": payload.reason, "is_false_positive": payload.is_false_positive}
    )
    db.add(audit)
    db.commit()
    db.refresh(incident)

    return {
        "message": f"Incident {incident_code} marked as {new_status}",
        "incident_code": incident_code,
        "status": new_status,
        "tester": payload.tester_name,
        "reason": payload.reason
    }
