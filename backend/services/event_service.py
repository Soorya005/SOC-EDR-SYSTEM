from backend.database import repositories


def list_events() -> list[dict]:
    return repositories.fetch_events()