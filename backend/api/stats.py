from fastapi import APIRouter

from services import stats_service

router = APIRouter(
    prefix="/stats",
    tags=["Statistics"],
)


@router.get("/summary")
def summary():
    """
    Dashboard summary.
    """
    return stats_service.get_summary()


@router.get("/trends")
def trends():
    """
    Daily alert trends.
    """
    return stats_service.get_trends()


@router.get("/heatmap")
def heatmap():
    """
    MITRE ATT&CK heatmap.
    """
    return stats_service.get_heatmap()


