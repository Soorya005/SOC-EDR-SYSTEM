from typing import Optional

from pydantic import BaseModel, ConfigDict
from enum import Enum

# EVENT MODELS

class EventCreate(BaseModel):
    model_config = ConfigDict(extra="allow")
    event_id: int
    host: Optional[str] = None
    process_name: Optional[str] = None
    parent_process: Optional[str] = None
    command_line: Optional[str] = None


class EventResponse(EventCreate):
    id: str

    model_config = ConfigDict(from_attributes=True)


# ALERT MODELS

class AlertCreate(BaseModel):
    rule_name: str
    severity: str = "Medium"

    technique_id: Optional[str] = None
    event_id: Optional[str] = None

    incident_id: Optional[str] = None

    ai_explanation: Optional[str] = None
    ai_recommendations: Optional[str] = None


class AlertResponse(AlertCreate):
    id: str
    status: str

    model_config = ConfigDict(from_attributes=True)



class AlertStatus(str, Enum):
    NEW = "New"
    INVESTIGATING = "Investigating"
    ESCALATED = "Escalated"
    CLOSED = "Closed"
    FALSE_POSITIVE = "False Positive"

class AlertStatusUpdate(BaseModel):
    status: AlertStatus

class AIExplanationUpdate(BaseModel):
    ai_explanation: str
    ai_recommendations: str


# INVESTIGATION MODELS

class InvestigationCreate(BaseModel):
    analyst_notes: str    


# DASHBOARD MODELS

class StatsSummary(BaseModel):
    total_alerts: int
    critical_alerts: int
    open_alerts: int