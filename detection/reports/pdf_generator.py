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


def generate_daily_report(stats: dict) -> bytes:
    """
    Generates a professional daily security report containing alert metrics,
    open incidents, MITRE ATT&CK techniques, and AI analysis.
    """
    logger.info("Generating Daily Security Report...")
    
    packet = io.BytesIO()
    c = canvas.Canvas(packet, pagesize=letter)
    
    width, height = letter
    
    # Palette
    primary_color = (0.1, 0.2, 0.4)     # Dark Blue
    secondary_color = (0.3, 0.3, 0.3)   # Gray
    accent_critical = (0.8, 0.2, 0.2)   # Red
    accent_high = (0.9, 0.5, 0.1)       # Orange
    accent_medium = (0.9, 0.7, 0.1)     # Yellow
    
    # Title Banner
    c.setFillColorRGB(*primary_color)
    c.rect(0, height - 100, width, 100, fill=True, stroke=False)
    
    # Title Text
    c.setFillColorRGB(1, 1, 1)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 55, "DAILY SECURITY REPORT")
    
    # Date Subtitle
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Generated Date: {stats.get('date', '')}")
    
    y = height - 140
    
    def add_section_header(title):
        nonlocal y
        y -= 10
        c.setFillColorRGB(*primary_color)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, title)
        y -= 6
        c.setStrokeColorRGB(*primary_color)
        c.setLineWidth(1)
        c.line(50, y, width - 50, y)
        y -= 20

    # 1. Executive Summary
    add_section_header("1. Executive Summary")
    
    # Draw metrics grid
    metrics = [
        ("Total Alerts", str(stats.get("total_alerts", 0)), (0.2, 0.4, 0.6)),
        ("Open Incidents", str(stats.get("open_incidents", 0)), (0.4, 0.4, 0.4)),
        ("Critical Alerts", str(stats.get("critical_alerts", 0)), accent_critical),
        ("High Alerts", str(stats.get("high_alerts", 0)), accent_high)
    ]
    
    box_width = 110
    box_height = 50
    spacing = 20
    start_x = 50
    
    for idx, (label, val, color) in enumerate(metrics):
        bx = start_x + idx * (box_width + spacing)
        by = y - box_height
        
        # Draw box background
        c.setFillColorRGB(*color)
        c.rect(bx, by, box_width, box_height, fill=True, stroke=False)
        
        # Draw Value
        c.setFillColorRGB(1, 1, 1)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(bx + box_width/2, by + 25, val)
        
        # Draw Label
        c.setFont("Helvetica", 9)
        c.drawCentredString(bx + box_width/2, by + 10, label)
        
    y -= (box_height + 25)
    
    # Severity distribution details
    c.setFillColorRGB(*secondary_color)
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Medium Severity Alerts: {stats.get('medium_alerts', 0)}  |  Low Severity Alerts: {stats.get('low_alerts', 0)}")
    y -= 30
    
    # 2. AI Security Analysis
    add_section_header("2. AI Security Analysis")
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 10)
    
    ai_summary = stats.get("ai_summary", "No significant alerts were recorded during this period.")
    import textwrap
    wrapped_summary = textwrap.wrap(ai_summary, width=95)
    for line in wrapped_summary:
        c.drawString(50, y, line)
        y -= 15
        if y < 60:
            c.showPage()
            y = height - 60
            
    y -= 20
    
    # 3. MITRE ATT&CK Techniques Observed
    add_section_header("3. MITRE ATT&CK Techniques Observed")
    techniques = stats.get("techniques", [])
    if not techniques:
        c.setFillColorRGB(*secondary_color)
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(50, y, "No MITRE ATT&CK techniques observed in the last 24 hours.")
        y -= 25
    else:
        # Table Headers
        c.setFillColorRGB(*secondary_color)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(50, y, "ID")
        c.drawString(120, y, "Technique Name")
        c.drawString(380, y, "Tactic")
        c.drawString(500, y, "Count")
        y -= 6
        c.setStrokeColorRGB(0.8, 0.8, 0.8)
        c.line(50, y, width - 50, y)
        y -= 15
        
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica", 10)
        for tech in techniques:
            if y < 60:
                c.showPage()
                y = height - 60
                # Redraw Headers on new page
                c.setFillColorRGB(*secondary_color)
                c.setFont("Helvetica-Bold", 10)
                c.drawString(50, y, "ID")
                c.drawString(120, y, "Technique Name")
                c.drawString(380, y, "Tactic")
                c.drawString(500, y, "Count")
                y -= 6
                c.line(50, y, width - 50, y)
                y -= 15
                c.setFillColorRGB(0, 0, 0)
                c.setFont("Helvetica", 10)
                
            c.drawString(50, y, tech.get("technique_id", "N/A"))
            
            name = tech.get("name") or "Unknown"
            if len(name) > 40:
                name = name[:37] + "..."
            c.drawString(120, y, name)
            
            tactic = tech.get("tactic") or "Unknown"
            c.drawString(380, y, tactic)
            c.drawString(500, y, str(tech.get("count", 0)))
            y -= 15

    y -= 20
    
    # 4. Actionable Recommendations
    add_section_header("4. Actionable Recommendations")
    c.setFillColorRGB(0, 0, 0)
    c.setFont("Helvetica", 10)
    
    recs = stats.get("recommendations", [])
    for idx, rec in enumerate(recs, start=1):
        if y < 60:
            c.showPage()
            y = height - 60
        wrapped_rec = textwrap.wrap(f"{idx}. {rec}", width=95)
        for line in wrapped_rec:
            c.drawString(50, y, line)
            y -= 15
            
    c.save()
    packet.seek(0)
    return packet.getvalue()