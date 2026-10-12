from rules.failed_signins import detect_repeated_failures
from schemas.events import IdentityEvent

def analyze_events(events: list[IdentityEvent]) -> list[dict]:
    """Run the available detection rules against validated events."""
    event_data = [
        event.model_dump(mode="json")
        for event in events
    ]
    return detect_repeated_failures(event_data)