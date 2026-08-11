from fastapi import APIRouter, HTTPException
from fastapi.responses import Response

from services import report_service
from fastapi.responses import FileResponse
import os

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)

@router.get("/")
def list_reports():
    return report_service.get_reports()

@router.get("/download/{filename}")
def download_report(filename: str):

    base = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..",
            "..",
            "detection",
            "reports",
            "output"
        )
    )

    path = os.path.join(base, filename)

    if not os.path.exists(path):
        raise HTTPException(404, "Report not found")

    return FileResponse(
        path,
        media_type="application/pdf",
        filename=filename
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


@router.post("/daily")
def generate_daily_report():
    """
    Generates a daily security summary report for the last 24 hours.
    """
    try:
        return report_service.generate_daily_report_service()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating daily report: {str(e)}")

