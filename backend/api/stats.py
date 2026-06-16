from fastapi import APIRouter

router = APIRouter()


@router.get("")
def get_stats() -> dict[str, int]:
    return {"alerts": 0, "events": 0}