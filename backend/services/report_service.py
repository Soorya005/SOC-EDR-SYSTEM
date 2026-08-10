import logging
import sqlite3
import os
import sys
from pathlib import Path

from database.repositories import list_reports, get_daily_report_data

def get_reports():
    return list_reports()

# Calculate PROJECT_ROOT from current file path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Dynamically add the detection module to path so we can import the PDF generator.
# NOTE: The IDE may show a false "missing import" error on the next line — this is safe to ignore.
# At runtime, sys.path is updated BEFORE the import, so it works correctly.
detection_path = str(PROJECT_ROOT / "detection")
if detection_path not in sys.path:
    sys.path.append(detection_path)

from reports.pdf_generator import generate_pdf_report, generate_daily_report  # noqa: E402

logger = logging.getLogger(__name__)

def generate_alert_report(alert_id: str) -> bytes:
    """
    Fetches alert and related event data, then generates a PDF report.
    Returns the PDF bytes.
    """
    db_path = PROJECT_ROOT / "backend" / "database" / "edr.db"
    
    if not os.path.exists(db_path):
        raise FileNotFoundError("Database not found.")
        
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        
        # Get Alert
        cursor = conn.execute("SELECT * FROM alerts WHERE id = ?", (alert_id,))
        alert = cursor.fetchone()
        
        if not alert:
            conn.close()
            raise ValueError(f"Alert {alert_id} not found.")
            
        alert_dict = dict(alert)
        
        # Get Event
        cursor = conn.execute("SELECT * FROM events WHERE id = ?", (alert_dict.get('event_id'),))
        event = cursor.fetchone()
        
        if event:
            event_dict = dict(event)
            # Merge event data into alert data for the report
            alert_dict.update({
                'host': event_dict.get('host'),
                'process_name': event_dict.get('process_name'),
                'parent_process': event_dict.get('parent_process'),
                'command_line': event_dict.get('command_line'),
            })
            
        conn.close()
        
        # Generate PDF
        pdf_bytes = generate_pdf_report(alert_dict)
        return pdf_bytes
        
    except Exception as e:
        logger.error(f"Error generating report: {e}")
        raise


def generate_daily_report_service() -> dict:
    """
    Query today's stats, build AI summaries and recommendations,
    generate the Daily Security Report PDF, save it, and return metadata.
    """
    from datetime import datetime
    stats = get_daily_report_data()
    
    # Format date
    today_str = datetime.now().strftime("%Y-%m-%d")
    stats["date"] = today_str
    
    # Build AI Summary
    total = stats["total_alerts"]
    critical = stats["critical_alerts"]
    high = stats["high_alerts"]
    
    if total == 0:
        ai_summary = "During this 24-hour monitoring cycle, the SOC-EDR system did not detect any security events. Endpoints remain stable, and no suspicious activities were logged."
    else:
        ai_summary = f"Over the last 24 hours, the detection engine processed a total of {total} security alerts. "
        if critical > 0 or high > 0:
            ai_summary += f"Of these alerts, {critical} were classified as CRITICAL and {high} as HIGH severity, requiring immediate response. "
        else:
            ai_summary += "All detected alerts were classified as low or medium severity. No critical threats were observed. "
        
        # Mention observed MITRE techniques
        if stats["techniques"]:
            tech_names = [t["name"] for t in stats["techniques"][:3] if t["name"]]
            if tech_names:
                ai_summary += f"The primary MITRE ATT&CK techniques detected include: {', '.join(tech_names)}. "
        
        ai_summary += "Based on correlation rules, we recommend prompt analysis of these events to prevent lateral movement or credential access."
        
    stats["ai_summary"] = ai_summary
    
    # Recommendations
    recommendations = [
        "Ensure all critical alerts are triaged and closed in the alerts dashboard.",
        "Review MITRE ATT&CK technique details to identify potential security gaps."
    ]
    if critical > 0:
        recommendations.insert(0, "IMMEDIATE ACTION REQUIRED: Investigate the critical security events detected on the endpoints.")
    if high > 0:
        recommendations.insert(1, "High-priority threat hunt: Analyze logs related to high severity incidents to ensure containment.")
        
    stats["recommendations"] = recommendations
    
    # Generate the PDF
    pdf_bytes = generate_daily_report(stats)
    
    # Save the PDF in detection/reports/output/
    output_dir = PROJECT_ROOT / "detection" / "reports" / "output"
    os.makedirs(output_dir, exist_ok=True)
    
    filename = f"Daily_Report_{today_str}.pdf"
    filepath = output_dir / filename
    
    with open(filepath, "wb") as f:
        f.write(pdf_bytes)
        
    download_url = f"http://127.0.0.1:8000/reports/download/{filename}"
    
    return {
        "filename": filename,
        "download_url": download_url
    }

