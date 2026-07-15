import logging
import sqlite3
import os
import sys
from pathlib import Path

# Calculate PROJECT_ROOT from current file path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

# Dynamically add the detection module to path so we can import the PDF generator.
# NOTE: The IDE may show a false "missing import" error on the next line — this is safe to ignore.
# At runtime, sys.path is updated BEFORE the import, so it works correctly.
detection_path = str(PROJECT_ROOT / "detection")
if detection_path not in sys.path:
    sys.path.append(detection_path)

from reports.pdf_generator import generate_pdf_report  # noqa: E402

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
