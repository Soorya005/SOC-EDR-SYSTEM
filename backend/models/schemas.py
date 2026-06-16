from pydantic import BaseModel


class Alert(BaseModel):
    title: str
    severity: str


class Event(BaseModel):
    event_type: str
    source: str


class Report(BaseModel):
    name: str


class Stats(BaseModel):
    alerts: int = 0
    events: int = 0