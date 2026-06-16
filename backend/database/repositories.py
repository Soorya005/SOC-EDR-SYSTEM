from backend.database.db import get_connection


def fetch_alerts() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute("SELECT id, title, severity, created_at FROM alerts ORDER BY id DESC")
        return [dict(row) for row in rows.fetchall()]


def fetch_events() -> list[dict]:
    with get_connection() as connection:
        rows = connection.execute("SELECT id, event_type, source, created_at FROM events ORDER BY id DESC")
        return [dict(row) for row in rows.fetchall()]