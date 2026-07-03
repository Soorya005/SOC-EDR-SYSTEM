from database import repositories
from models.schemas import EventCreate


def create_event(event: EventCreate) -> str:
    """
    Store a new Sysmon event.
    """

    return repositories.create_event(event.model_dump())


def get_event(event_id: str):
    """
    Retrieve a single event.
    """

    return repositories.get_event(event_id)


def list_events():
    """
    Return all stored events.
    """

    return repositories.list_events()

def delete_event(event_id: str):
    """
    Delete an event.
    """
    repositories.delete_event(event_id)
