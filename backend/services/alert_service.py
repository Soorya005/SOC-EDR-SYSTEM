from backend.database import repositories


def list_alerts() -> list[dict]:
    return repositories.fetch_alerts()