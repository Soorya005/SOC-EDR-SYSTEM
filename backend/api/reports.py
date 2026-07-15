from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from services import report_service

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)

@router.get("/alerts/{alert_id}/pdf")
def get_alert_pdf(alert_id: str):
    """
    Generates and returns a PDF incident report for the specified alert.
    """
    try:
        pdf_bytes = report_service.generate_alert_report(alert_id)
        
        return Response(
            content=pdf_bytes, 
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=incident_report_{alert_id}.pdf"}
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error generating report")
