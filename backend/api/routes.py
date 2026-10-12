from pathlib import Path
import json
from fastapi import APIRouter, HTTPException
from schemas.events import IdentityEvent, AnalyzeRequest, Finding
from services.analysis import analyze_events
from services.db_service import (
    setup_database,
    save_events_to_db,
    save_findings_to_db,
    get_all_findings_from_db,
    get_finding_by_id_from_db,
)

router = APIRouter()

# Initialize SQLite database tables on startup
setup_database()

# Locate data/synthetic_identity_events.json from project root
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SAMPLE_DATA = ROOT_DIR / "data" / "synthetic_identity_events.json"

def load_sample_events() -> list[IdentityEvent]:
    if not SAMPLE_DATA.exists():
        raise HTTPException(
            status_code=500,
            detail=f"Synthetic dataset not found at {SAMPLE_DATA}. Check the data folder.",
        )
    try:
        raw_events = json.loads(
            SAMPLE_DATA.read_text(encoding="utf-8")
        )
        if not isinstance(raw_events, list):
            raise ValueError("Expected a JSON array.")
        return [
            IdentityEvent.model_validate(item)
            for item in raw_events
        ]
    except (ValueError, TypeError) as exc:
        raise HTTPException(
            status_code=500,
            detail="The synthetic dataset contains invalid data.",
        ) from exc

@router.get("/health")
def health():
    return {"status": "healthy"}

@router.get(
    "/api/v1/events",
    response_model=list[IdentityEvent],
)
def get_events():
    events = load_sample_events()
    # Save sample events to SQLite upon loading
    save_events_to_db([e.model_dump(mode="json") for e in events])
    return events

@router.post(
    "/api/v1/analyze",
    response_model=list[Finding],
)
def analyze(request: AnalyzeRequest):
    events = (
        request.events
        if request.events is not None
        else load_sample_events()
    )
    # Persist events to SQLite
    event_dicts = [e.model_dump(mode="json") for e in events]
    save_events_to_db(event_dicts)

    # Run detection rules
    raw_findings = analyze_events(events)
    
    formatted_findings = []
    for index, raw in enumerate(raw_findings, start=1):
        formatted_findings.append({
            "finding_id": f"F-{index:03d}",
            **raw,
        })
    
    # Save findings to SQLite
    save_findings_to_db(formatted_findings)
    return get_all_findings_from_db()

@router.get(
    "/api/v1/findings",
    response_model=list[Finding],
)
def get_findings():
    return get_all_findings_from_db()

@router.get(
    "/api/v1/findings/{finding_id}",
    response_model=Finding,
)
def get_finding_detail(finding_id: str):
    finding = get_finding_by_id_from_db(finding_id)
    if not finding:
        raise HTTPException(
            status_code=404,
            detail=f"Finding {finding_id} not found. Run POST /api/v1/analyze first."
        )
    return finding