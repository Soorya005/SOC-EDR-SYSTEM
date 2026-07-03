from fastapi import APIRouter, HTTPException, status

from models.schemas import EventCreate
from services import event_service

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_event(event: EventCreate):
    """
    Store a new Sysmon event.
    """

    event_id = event_service.create_event(event)

    return {
        "message": "Event created successfully",
        "event_id": event_id,
    }


@router.get("/")
def get_events():
    """
    Return all events.
    """

    return event_service.list_events()


@router.get("/{event_id}")
def get_event(event_id: str):
    """
    Return a single event.
    """

    event = event_service.get_event(event_id)

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    return event


@router.delete("/{event_id}")
def delete_event(event_id: str):
    """
    Delete an event.
    """

    event = event_service.get_event(event_id)

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found",
        )

    event_service.delete_event(event_id)

    return {
        "message": "Event deleted successfully"
    }