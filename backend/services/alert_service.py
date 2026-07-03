from database import repositories
from models.schemas import (
    AlertCreate,
    AlertStatusUpdate,
    AIExplanationUpdate,
)


def create_alert(alert: AlertCreate) -> str:
    """
    Validate and store a new alert.
    """

    # Business Rule:
    # Every alert must belong to an existing event.

    event = repositories.get_event(alert.event_id)

    if event is None:
        raise ValueError(
            f"Event {alert.event_id} does not exist."
        )

    return repositories.create_alert(
        alert.model_dump()
    )


def get_alert(alert_id: str):
    """
    Return one alert.
    """

    return repositories.get_alert(alert_id)


def list_alerts(
    status=None,
    severity=None,
):
    """
    Return alerts with optional filters.
    """

    return repositories.list_alerts(
        status,
        severity,
    )


def update_alert_status(
    alert_id: str,
    status_update: AlertStatusUpdate,
):
    """
    Update alert workflow status.
    """

    repositories.update_alert_status(
        alert_id,
        status_update.status,
    )


def update_ai_explanation(
    alert_id: str,
    ai_update: AIExplanationUpdate,
):
    """
    Save AI explanation.
    """

    repositories.update_ai_explanation(
        alert_id,
        ai_update.ai_explanation,
        ai_update.ai_recommendations,
    )


def delete_alert(alert_id: str):
    """
    Delete an alert.
    """

    repositories.delete_alert(alert_id)
