import json
import uuid
from datetime import datetime

VALID_ALERT_STATUSES = {
    "New",
    "Investigating",
    "Escalated",
    "Closed",
    "False Positive",
}

from .db import get_connection

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

REPORT_FOLDER = os.path.join(
    BASE_DIR,
    "detection",
    "reports",
    "output"
)

def list_reports():
    reports = []

    if not os.path.exists(REPORT_FOLDER):
        return reports

    for filename in os.listdir(REPORT_FOLDER):
        if filename.endswith(".pdf"):
            path = os.path.join(REPORT_FOLDER, filename)

            reports.append({
                "report_name": filename,
                "type": "PDF",
                "generated_by": "AI Engine",
                "created": datetime.fromtimestamp(
                    os.path.getctime(path)
                ).strftime("%Y-%m-%d %H:%M"),
                "status": "Completed"
            })

    reports.sort(
        key=lambda r: r["created"],
        reverse=True
    )

    return reports

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
        SELECT 
            a.id,
            a.rule_name,
            a.severity,
            a.status,
            a.technique_id,
            a.event_id,
            a.incident_id,
            a.ai_explanation,
            a.ai_recommendations,
            a.created_at,
            a.updated_at,
            e.host,
            e.process_name,
            e.parent_process,
            e.command_line,
            mt.name AS technique_name,
            mt.tactic
        FROM alerts a
        LEFT JOIN events e ON a.event_id = e.id
        LEFT JOIN mitre_techniques mt ON a.technique_id = mt.technique_id
        WHERE a.id = ?
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

    query = """
        SELECT a.*, e.host
        FROM alerts a
        LEFT JOIN events e ON a.event_id = e.id
        WHERE 1=1
    """
    params = []

    if status:
        query += " AND a.status = ?"
        params.append(status)

    if severity:
        query += " AND a.severity = ?"
        params.append(severity)

    query += " ORDER BY a.created_at DESC"

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

        # Frontend expects this field
        "active_incidents": open_alerts,

        # Placeholder values (replace with real logic later)
        "monitored_endpoints": 1,

        "backend_online": True,
        "database_online": True,
        "ai_online": True,
        "sysmon_running": True,

        "last_updated": datetime.now().strftime("%d %b %Y %H:%M")
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

# ============================================================
# INCIDENTS REPOSITORY
# ============================================================

def create_incident(incident: dict):
    """
    Store a new incident.
    """

    conn = get_connection()

    conn.execute(
        """
        INSERT INTO incidents (
            id,
            host,
            severity,
            status
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            incident["id"],
            incident["host"],
            incident["severity"],
            incident.get("status", "Open"),
        ),
    )

    conn.commit()
    conn.close()


def list_incidents():
    """
    Return all incidents.
    """

    conn = get_connection()

    rows = conn.execute(
        """
        SELECT *
        FROM incidents
        ORDER BY created_at DESC
        """
    ).fetchall()

    conn.close()

    return [dict(r) for r in rows]


def get_incident(incident_id: str):
    conn = get_connection()

    row = conn.execute(
        """
        SELECT *
        FROM incidents
        WHERE id = ?
        """,
        (incident_id,),
    ).fetchone()

    conn.close()

    return dict(row) if row else None


def create_incident(incident: dict):
    conn = get_connection()

    conn.execute(
        """
        INSERT INTO incidents (
            id,
            host,
            severity,
            status
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            incident["id"],
            incident["host"],
            incident["severity"],
            incident.get("status", "Open"),
        ),
    )

    conn.commit()
    conn.close()


def get_daily_report_data():
    """
    Query database for alerts and incidents in the last 24 hours to compile daily report stats.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # 1. Total alerts in last 24 hours
    cursor.execute("SELECT COUNT(*) FROM alerts WHERE created_at >= datetime('now', '-1 day')")
    total_alerts = cursor.fetchone()[0]

    # 2. Alerts by severity in last 24 hours
    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity = 'Critical' AND created_at >= datetime('now', '-1 day')")
    critical_alerts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity = 'High' AND created_at >= datetime('now', '-1 day')")
    high_alerts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity = 'Medium' AND created_at >= datetime('now', '-1 day')")
    medium_alerts = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alerts WHERE severity = 'Low' AND created_at >= datetime('now', '-1 day')")
    low_alerts = cursor.fetchone()[0]

    # 3. Open incidents in last 24 hours
    cursor.execute("SELECT COUNT(*) FROM incidents WHERE status != 'Closed' AND created_at >= datetime('now', '-1 day')")
    open_incidents = cursor.fetchone()[0]

    # 4. MITRE techniques observed in last 24 hours
    cursor.execute(
        """
        SELECT a.technique_id, mt.name, mt.tactic, COUNT(*) as count
        FROM alerts a
        LEFT JOIN mitre_techniques mt ON a.technique_id = mt.technique_id
        WHERE a.technique_id IS NOT NULL AND a.created_at >= datetime('now', '-1 day')
        GROUP BY a.technique_id, mt.name, mt.tactic
        ORDER BY count DESC
        """
    )
    techniques = [dict(row) for row in cursor.fetchall()]

    conn.close()

    return {
        "total_alerts": total_alerts,
        "critical_alerts": critical_alerts,
        "high_alerts": high_alerts,
        "medium_alerts": medium_alerts,
        "low_alerts": low_alerts,
        "open_incidents": open_incidents,
        "techniques": techniques
    }


def get_mitre_techniques_report():
    """
    Query database for MITRE techniques and associated alerts, returns alert counts
    and maximum severity. Ordered by alert count descending.
    """
    conn = get_connection()
    cursor = conn.execute(
        """
        SELECT 
            mt.technique_id, 
            mt.name, 
            mt.tactic, 
            COUNT(a.id) AS alert_count,
            CASE MAX(
                CASE a.severity
                    WHEN 'Critical' THEN 4
                    WHEN 'High' THEN 3
                    WHEN 'Medium' THEN 2
                    WHEN 'Low' THEN 1
                    ELSE 0
                END
            )
                WHEN 4 THEN 'Critical'
                WHEN 3 THEN 'High'
                WHEN 2 THEN 'Medium'
                WHEN 1 THEN 'Low'
                ELSE 'Low'
            END AS severity
        FROM alerts a
        JOIN mitre_techniques mt ON a.technique_id = mt.technique_id
        GROUP BY mt.technique_id, mt.name, mt.tactic
        ORDER BY alert_count DESC
        """
    )
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
