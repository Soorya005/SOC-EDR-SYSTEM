from database import repositories


def list_incidents():
    """
    Return all incidents.
    """
    return repositories.list_incidents()


def get_incident(incident_id: str):
    """
    Return one incident.
    """
    return repositories.get_incident(incident_id)