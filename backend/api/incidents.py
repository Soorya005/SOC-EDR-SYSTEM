from fastapi import APIRouter, HTTPException

from services import incident_service

router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


@router.get("/")
def get_incidents():
    """
    Return all incidents.
    """
    return incident_service.list_incidents()


@router.get("/{incident_id}")
def get_incident(incident_id: str):
    """
    Return a single incident.
    """

    incident = incident_service.get_incident(incident_id)

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    return incident