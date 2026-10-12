from datetime import datetime, timezone
from db.database import SessionLocal, init_db
from db.models import DBEvent, DBFinding

def setup_database():
    init_db()

def _parse_dt(dt_val):
    """Helper to convert string or datetime to a timezone-aware datetime object."""
    if isinstance(dt_val, datetime):
        if dt_val.tzinfo is None:
            return dt_val.replace(tzinfo=timezone.utc)
        return dt_val
    if isinstance(dt_val, str):
        try:
            parsed = datetime.fromisoformat(dt_val.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed
        except (ValueError, TypeError):
            return datetime.now(timezone.utc)
    return datetime.now(timezone.utc)

def save_events_to_db(events_data: list[dict]):
    db = SessionLocal()
    try:
        for e in events_data:
            existing = db.query(DBEvent).filter(DBEvent.event_id == e["event_id"]).first()
            if not existing:
                db_event = DBEvent(
                    event_id=e["event_id"],
                    timestamp=_parse_dt(e["timestamp"]),
                    user=e["user"],
                    event_type=e["event_type"],
                    result=e["result"],
                    ip_address=e.get("ip_address"),
                    source=e.get("source", "synthetic")
                )
                db.add(db_event)
        db.commit()
    finally:
        db.close()

def save_findings_to_db(findings_data: list[dict]):
    db = SessionLocal()
    try:
        db.query(DBFinding).delete()
        for f in findings_data:
            db_finding = DBFinding(
                finding_id=f["finding_id"],
                rule_id=f["rule_id"],
                severity=f["severity"],
                confidence=f["confidence"],
                user=f["user"],
                event_count=f["event_count"],
                window_minutes=f["window_minutes"],
                first_seen=_parse_dt(f["first_seen"]),
                evidence=f["evidence"],
                summary=f["summary"]
            )
            db.add(db_finding)
        db.commit()
    finally:
        db.close()

def get_all_findings_from_db() -> list[DBFinding]:
    db = SessionLocal()
    try:
        return db.query(DBFinding).all()
    finally:
        db.close()

def get_finding_by_id_from_db(finding_id: str) -> DBFinding | None:
    db = SessionLocal()
    try:
        return db.query(DBFinding).filter(DBFinding.finding_id == finding_id).first()
    finally:
        db.close()