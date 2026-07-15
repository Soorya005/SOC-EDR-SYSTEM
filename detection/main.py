import asyncio
import logging
import httpx
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import BACKEND_API_URL
from sysmon.listener import listen_async
from sigma.rule_loader import load_sigma_rules
from sigma.engine import SigmaEngine
from ai_triage.ollama_client import get_ai_explanation
from correlator import AlertCorrelator
from mitre.loader import load_mitre_data
from mitre.mapper import MitreMapper
from reports.pdf_generator import generate_incident_report

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

GENERATED_INCIDENTS = set()  # tracks incident IDs already reported, avoids duplicate PDFs

def maybe_generate_incident_report(incident_id: str, correlator: AlertCorrelator):
    """
    Auto-generates a PDF report the first time an incident reaches 2+ correlated alerts.
    """
    alerts = correlator.get_incident_alerts(incident_id)
    if len(alerts) >= 2 and incident_id not in GENERATED_INCIDENTS:
        try:
            pdf_bytes = generate_incident_report(alerts)
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports", "output")
            os.makedirs(output_dir, exist_ok=True)
            filepath = os.path.join(output_dir, f"incident_{incident_id}.pdf")
            with open(filepath, "wb") as f:
                f.write(pdf_bytes)
            GENERATED_INCIDENTS.add(incident_id)
            logger.info(f"Auto-generated incident report: {filepath}")
        except Exception as e:
            logger.error(f"Failed to auto-generate incident report: {e}")

async def process_event(event: dict, engine: SigmaEngine, correlator: AlertCorrelator, mapper: MitreMapper):
    logger.info(f"Processing event: {event.get('event_id')} from {event.get('host')}")

    matches = engine.match_event(event)

    if not matches:
        return

    logger.warning(f"Event matched {len(matches)} Sigma rules!")

    async with httpx.AsyncClient() as client:
        try:
            evt_resp = await client.post(f"{BACKEND_API_URL}/events/", json=event)
            if evt_resp.status_code != 201:
                logger.error(f"Failed to create event: {evt_resp.text}")
                return

            event_uuid = evt_resp.json().get("event_id")
            if not event_uuid:
                logger.error("Backend did not return event_id, aborting alert creation.")
                return

        except Exception as e:
            logger.error(f"Error communicating with backend (events): {e}")
            return

        for match in matches:
            mitre_info = mapper.get_technique_details(match["technique_id"]) or {}

            alert_payload = {
                "rule_name": match["rule_name"],
                "severity": match["severity"],
                "technique_id": match["technique_id"],
                "technique_name": mitre_info.get("name"),
                "tactic": mitre_info.get("tactic"),
                "event_id": event_uuid,
            }

            incident_id = correlator.correlate_alert(alert_payload, event)
            alert_payload["incident_id"] = incident_id

            try:
                alt_resp = await client.post(f"{BACKEND_API_URL}/alerts/", json=alert_payload)
                if alt_resp.status_code != 201:
                    logger.error(f"Failed to create alert: {alt_resp.text}")
                    continue

                alert_uuid = alt_resp.json().get("alert_id")
                logger.info(f"Created alert {alert_uuid} for rule {match['rule_name']}")

                logger.info("Requesting AI triage explanation...")
                ai_result = await get_ai_explanation(alert_payload, event)

                ai_payload = {
                    "ai_explanation": ai_result["explanation"],
                    "ai_recommendations": ai_result["recommendations"]
                }

                ai_resp = await client.patch(
                    f"{BACKEND_API_URL}/alerts/{alert_uuid}/ai",
                    json=ai_payload
                )

                if ai_resp.status_code == 200:
                    logger.info(f"Successfully updated alert {alert_uuid} with AI triage.")
                    alert_payload["ai_explanation"] = ai_result["explanation"]
                    alert_payload["ai_recommendations"] = ai_result["recommendations"]
                else:
                    logger.error(f"Failed to update AI triage: {ai_resp.text}")

                maybe_generate_incident_report(incident_id, correlator)

            except Exception as e:
                logger.error(f"Error processing alert pipeline: {e}")

async def main():
    logger.info("Starting SOC-EDR Detection Engine...")

    load_mitre_data()

    rules = load_sigma_rules()
    
    from mitre.loader import backfill_missing_techniques
    backfill_missing_techniques(rules)
    
    if not rules:
        logger.warning("No Sigma rules loaded. Engine will not detect anything.")

    engine = SigmaEngine(rules)
    correlator = AlertCorrelator()
    mapper = MitreMapper()

    main_loop = asyncio.get_running_loop()

    def event_callback(normalized_event):
        asyncio.run_coroutine_threadsafe(
            process_event(normalized_event, engine, correlator, mapper),
            main_loop
        )

    logger.info("Starting Sysmon listener...")
    await listen_async(event_callback)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Detection Engine stopped by user.")