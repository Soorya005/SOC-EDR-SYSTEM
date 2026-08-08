from fastapi import APIRouter
from services import mitre_service

router = APIRouter(
    prefix="/mitre",
    tags=["MITRE ATT&CK"],
)

@router.get("")
@router.get("/")
def get_mitre_techniques():
    """
    Returns live alert counts and severity grouped by MITRE ATT&CK Technique.
    """
    return mitre_service.get_mitre_techniques()
