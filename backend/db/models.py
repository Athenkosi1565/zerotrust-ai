from sqlalchemy import Column, String, Integer, DateTime, JSON
from db.database import Base

class DBEvent(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    user = Column(String, index=True, nullable=False)
    event_type = Column(String, nullable=False)
    result = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    source = Column(String, default="synthetic")

class DBFinding(Base):
    __tablename__ = "findings"

    finding_id = Column(String, primary_key=True, index=True)
    rule_id = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    confidence = Column(String, nullable=False)
    user = Column(String, index=True, nullable=False)
    event_count = Column(Integer, nullable=False)
    window_minutes = Column(Integer, nullable=False)
    first_seen = Column(DateTime, nullable=False)
    evidence = Column(JSON, nullable=False)  # Stores list of event IDs as JSON array
    summary = Column(String, nullable=False)