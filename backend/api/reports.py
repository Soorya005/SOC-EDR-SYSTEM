from fastapi import APIRouter

router = APIRouter()


@router.get("")
def list_reports() -> list[dict[str, str]]:
    return []