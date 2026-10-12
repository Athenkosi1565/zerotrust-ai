
from app.rules.failed_signins import detect_repeated_failures


def test_detects_five_failed_signins():
    events = [
        {
            "event_id": f"EVT-{i}",
            "timestamp": f"2026-10-12T08:{i * 2:02d}:00Z",
            "user": "alex.morgan@example.test",
            "event_type": "signin",
            "result": "failure",
        }
        for i in range(5)
    ]

    findings = detect_repeated_failures(events)

    assert len(findings) == 1
    assert findings[0]["rule_id"] == "ID-001"
    assert findings[0]["event_count"] == 5


def test_ignores_four_failed_signins():
    events = [
        {
            "event_id": f"EVT-{i}",
            "timestamp": f"2026-10-12T08:0{i}:00Z",
            "user": "alex.morgan@example.test",
            "event_type": "signin",
            "result": "failure",
        }
        for i in range(4)
    ]

    assert detect_repeated_failures(events) == []
