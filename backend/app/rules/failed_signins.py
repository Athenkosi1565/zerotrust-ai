
from collections import defaultdict
from datetime import datetime, timedelta, timezone


def detect_repeated_failures(
    events: list[dict],
    threshold: int = 5,
    window_minutes: int = 10,
) -> list[dict]:
    """Detect repeated failed sign-ins within a time window."""
    failures = defaultdict(list)
    window = timedelta(minutes=window_minutes)

    for event in events:
        if event.get("event_type") != "signin":
            continue

        if event.get("result") != "failure":
            continue

        user = event.get("user")
        timestamp = event.get("timestamp")

        if not user or not timestamp:
            continue

        try:
            parsed = datetime.fromisoformat(
                timestamp.replace("Z", "+00:00")
            )
        except (ValueError, TypeError):
            continue

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)

        failures[user].append((parsed, event))

    findings = []

    for user, user_events in failures.items():
        user_events.sort(key=lambda item: item[0])

        for index, (start_time, _) in enumerate(user_events):
            matching = [
                event
                for timestamp, event in user_events[index:]
                if timestamp - start_time <= window
            ]

            if len(matching) >= threshold:
                findings.append({
                    "rule_id": "ID-001",
                    "severity": "medium",
                    "confidence": "medium",
                    "user": user,
                    "event_count": len(matching),
                    "window_minutes": window_minutes,
                    "first_seen": matching[0]["timestamp"],
                    "evidence": [
                        event["event_id"] for event in matching
                    ],
                    "summary": (
                        f"{len(matching)} failed sign-ins for {user} "
                        f"within {window_minutes} minutes."
                    ),
                })
                break

    return findings
