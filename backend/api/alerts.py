from typing import Optional

from fastapi import APIRouter, HTTPException, status

from models.schemas import (
    AlertCreate,
    AlertStatusUpdate,
    AIExplanationUpdate,
)

from services import alert_service

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
def create_alert(alert: AlertCreate):

    try:
        alert_id = alert_service.create_alert(alert)

        return {
            "message": "Alert created successfully",
            "alert_id": alert_id,
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
        
@router.get("/")
def get_alerts(
    status: Optional[str] = None,
    severity: Optional[str] = None,
):

    return alert_service.list_alerts(
        status=status,
        severity=severity,
    )

@router.get("/{alert_id}")
def get_alert(alert_id: str):

    alert = alert_service.get_alert(alert_id)

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    return alert

@router.patch("/{alert_id}/status")
def update_status(
    alert_id: str,
    status_update: AlertStatusUpdate,
):

    try:
        alert_service.update_alert_status(
            alert_id,
            status_update,
        )

        return {
            "message": "Alert status updated"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    
@router.patch("/{alert_id}/ai")
def update_ai(
    alert_id: str,
    ai_update: AIExplanationUpdate,
):

    alert_service.update_ai_explanation(
        alert_id,
        ai_update,
    )

    return {
        "message": "AI explanation updated"
    }

@router.delete("/{alert_id}")
def delete_alert(alert_id: str):

    alert_service.delete_alert(alert_id)

    return {
        "message": "Alert deleted"
    }
