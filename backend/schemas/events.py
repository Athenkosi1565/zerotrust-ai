from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

class IdentityEvent(BaseModel):
    event_id: str = Field(min_length=1)
    timestamp: datetime
    user: str = Field(min_length=1)
    event_type: Literal["signin", "role_assignment"]
    result: Literal["success", "failure", "assigned"]
    ip_address: str | None = None
    source: str = "synthetic"

class AnalyzeRequest(BaseModel):
    events: list[IdentityEvent] | None = None

class Finding(BaseModel):
    finding_id: str
    rule_id: str
    severity: str
    confidence: str
    user: str
    event_count: int
    window_minutes: int
    first_seen: datetime
    evidence: list[str]
    summary: str