from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
import logging

logger = logging.getLogger(__name__)

def generate_pdf_report(report_data: dict) -> bytes:
    """
    Generates a PDF report for an incident/alert using ReportLab.
    Returns the PDF as bytes.
    """
    logger.info("Generating PDF report...")
    
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    
    # Starting coordinates
    x = 50
    y = 750
    line_height = 15
    
    def add_line(text, is_bold=False):
        nonlocal y
        if is_bold:
            c.setFont("Helvetica-Bold", 12)
        else:
            c.setFont("Helvetica", 10)
            
        c.drawString(x, y, str(text))
        y -= line_height
        
        if y < 50:
            c.showPage()
            y = 750

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, "SOC-EDR Incident Report")
    y -= 30
    
    # Alert Details
    add_line("Alert Details", is_bold=True)
    add_line(f"Alert ID: {report_data.get('id') or report_data.get('alert_id', 'N/A')}")
    add_line(f"Rule Name: {report_data.get('rule_name', 'N/A')}")
    add_line(f"Severity: {report_data.get('severity', 'N/A')}")
    add_line(f"Technique ID: {report_data.get('technique_id', 'N/A')}")
    y -= line_height
    
    # Event Details
    add_line("Event Context", is_bold=True)
    add_line(f"Host: {report_data.get('host', 'N/A')}")
    add_line(f"Process: {report_data.get('process_name', 'N/A')}")
    add_line(f"Parent Process: {report_data.get('parent_process', 'N/A')}")
    add_line(f"Command Line: {report_data.get('command_line', 'N/A')}")
    y -= line_height
    
    # AI Analysis
    add_line("AI Analysis", is_bold=True)
    
    explanation = report_data.get('ai_explanation', 'N/A')
    # Simple text wrapping for the explanation
    import textwrap
    wrapped_exp = textwrap.wrap(f"Explanation: {explanation}", width=80)
    for line in wrapped_exp:
        add_line(line)
        
    y -= line_height
    
    recs = report_data.get('ai_recommendations', 'N/A')
    wrapped_recs = textwrap.wrap(f"Recommendations: {recs}", width=80)
    for line in wrapped_recs:
        add_line(line)
        
    c.save()
    packet.seek(0)
    return packet.getvalue()


def generate_incident_report(alerts: list) -> bytes:
    """
    Generates a PDF report covering multiple correlated alerts (one incident).
    """
    logger.info(f"Generating incident report for {len(alerts)} alerts...")
    
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    
    # Starting coordinates
    x = 50
    y = 750
    line_height = 15
    
    def add_line(text, is_bold=False):
        nonlocal y
        if is_bold:
            c.setFont("Helvetica-Bold", 12)
        else:
            c.setFont("Helvetica", 10)
            
        c.drawString(x, y, str(text))
        y -= line_height
        
        if y < 50:
            c.showPage()
            y = 750

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x, y, "SOC-EDR Incident Report")
    y -= 30
    
    # Alert Details
    add_line(f"Total Correlated Alerts: {len(alerts)}", is_bold=True)
    y -= line_height
    
    import textwrap
    
    for i, alert in enumerate(alerts, start=1):
        add_line(f"Alert {i}", is_bold=True)
        add_line(f"Rule Name: {alert.get('rule_name', 'N/A')}")
        add_line(f"Severity: {alert.get('severity', 'N/A')}")
        add_line(f"Technique ID: {alert.get('technique_id', 'N/A')}")
        add_line(f"Technique Name: {alert.get('technique_name', 'N/A')}")
        
        explanation = alert.get('ai_explanation', 'N/A')
        for line in textwrap.wrap(f"Explanation: {explanation}", width=80):
            add_line(line)
            
        recs = alert.get('ai_recommendations', 'N/A')
        for line in textwrap.wrap(f"Recommendations: {recs}", width=80):
            add_line(line)
            
        y -= line_height
        
    c.save()
    packet.seek(0)
    return packet.getvalue()