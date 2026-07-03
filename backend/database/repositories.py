import json
import uuid

VALID_ALERT_STATUSES = {
    "New",
    "Investigating",
    "Escalated",
    "Closed",
    "False Positive",
}

from .db import get_connection


# ==========================================================
# EVENTS REPOSITORY
# ==========================================================

def create_event(event: dict):
    """
    Store a normalized Sysmon event in the database.
    """

    conn = get_connection()

    event_uuid = str(uuid.uuid4())

    conn.execute(
        """
        INSERT INTO events (
            id,
            event_id,
            host,
            process_name,
            parent_process,
            command_line,
            raw_json
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event_uuid,
            event["event_id"],
            event.get("host"),
            event.get("process_name"),
            event.get("parent_process"),
            event.get("command_line"),
            json.dumps(event),
        ),
    )

    conn.commit()
    conn.close()

    return event_uuid


def get_event(event_uuid: str):
    """
    Retrieve a single event by its UUID.
    """

    conn = get_connection()

    cursor = conn.execute(
        """
        SELECT *
        FROM events
        WHERE id = ?
        """,
        (event_uuid,),
    )

    row = cursor.fetchone()

    conn.close()

    return dict(row) if row else None


def list_events():
    """
    Return all stored events.
    """

    conn = get_connection()

    cursor = conn.execute(
        """
        SELECT *
        FROM events
        ORDER BY created_at DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

def delete_event(event_id: str):
    conn = get_connection()

    conn.execute(
        """
        DELETE FROM events
        WHERE id = ?
        """,
        (event_id,),
    )

    conn.commit()
    conn.close()


# ==========================================================
# ALERTS REPOSITORY
# ==========================================================

def create_alert(alert: dict):
    """
    Store a Sigma-generated alert in the database.
    """

    conn = get_connection()

    alert_uuid = str(uuid.uuid4())

    conn.execute(
        """
        INSERT INTO alerts (
            id,
            rule_name,
            severity,
            status,
            technique_id,
            event_id,
            incident_id,
            ai_explanation,
            ai_recommendations
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            alert_uuid,
            alert["rule_name"],
            alert.get("severity", "Medium"),
            alert.get("status", "New"),
            alert.get("technique_id"),
            alert.get("event_id"),
            alert.get("incident_id"),
            alert.get("ai_explanation"),
            alert.get("ai_recommendations"),
        ),
    )

    conn.commit()
    conn.close()

    return alert_uuid


def get_alert(alert_uuid: str):
    """
    Retrieve one alert by UUID.
    """

    conn = get_connection()

    cursor = conn.execute(
        """
        SELECT *
        FROM alerts
        WHERE id = ?
        """,
        (alert_uuid,),
    )

    row = cursor.fetchone()

    conn.close()

    return dict(row) if row else None


def list_alerts(status=None, severity=None):
    """
    Return all alerts.
    Optional filtering by status and severity.
    """

    conn = get_connection()

    query = "SELECT * FROM alerts WHERE 1=1"
    params = []

    if status:
        query += " AND status = ?"
        params.append(status)

    if severity:
        query += " AND severity = ?"
        params.append(severity)

    query += " ORDER BY created_at DESC"

    cursor = conn.execute(query, params)

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

def update_alert_status(alert_id: str, status: str):
    """
    Update the workflow status of an alert.
    """

    if status not in VALID_ALERT_STATUSES:
        raise ValueError(f"Invalid alert status: {status}")

    conn = get_connection()

    conn.execute(
        """
        UPDATE alerts
        SET status = ?,
            updated_at = datetime('now')
        WHERE id = ?
        """,
        (status, alert_id),
    )

    conn.commit()
    conn.close()

def update_ai_explanation(
    alert_id: str,
    explanation: str,
    recommendations: str,
):
    """
    Save AI-generated explanation and recommendations.
    """

    conn = get_connection()

    conn.execute(
        """
        UPDATE alerts
        SET
            ai_explanation = ?,
            ai_recommendations = ?,
            updated_at = datetime('now')
        WHERE id = ?
        """,
        (
            explanation,
            recommendations,
            alert_id,
        ),
    )

    conn.commit()
    conn.close()

def delete_alert(alert_id: str):
    """
    Delete an alert.
    """

    conn = get_connection()

    conn.execute(
        """
        DELETE FROM alerts
        WHERE id = ?
        """,
        (alert_id,),
    )

    conn.commit()
    conn.close()

def get_summary_stats():
    """
    Return dashboard summary statistics.
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM alerts")
    total_alerts = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM alerts WHERE severity='Critical'"
    )
    critical_alerts = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM alerts
        WHERE status != 'Closed'
        """
    )
    open_alerts = cursor.fetchone()[0]

    conn.close()

    return {
        "total_alerts": total_alerts,
        "critical_alerts": critical_alerts,
        "open_alerts": open_alerts,
    }

def get_alert_trends():
    """
    Return daily alert counts.
    """

    conn = get_connection()

    cursor = conn.execute(
        """
        SELECT
            DATE(created_at) AS date,
            COUNT(*) AS count
        FROM alerts
        GROUP BY DATE(created_at)
        ORDER BY DATE(created_at)
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

def get_heatmap_data():
    """
    Return alert count by MITRE technique.
    """

    conn = get_connection()

    cursor = conn.execute(
        """
        SELECT
            technique_id,
            COUNT(*) AS count
        FROM alerts
        WHERE technique_id IS NOT NULL
        GROUP BY technique_id
        ORDER BY count DESC
        """
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]

