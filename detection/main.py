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

GENERATED_INCIDENTS = set()


def maybe_generate_incident_report(
    incident_id: str,
    correlator: AlertCorrelator
):
    """
    Auto-generates a PDF report the first time an incident
    reaches 2+ correlated alerts.
    """

    alerts = correlator.get_incident_alerts(incident_id)

    if len(alerts) >= 2 and incident_id not in GENERATED_INCIDENTS:
        try:
            pdf_bytes = generate_incident_report(alerts)

            output_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "reports",
                "output"
            )

            os.makedirs(output_dir, exist_ok=True)

            filepath = os.path.join(
                output_dir,
                f"incident_{incident_id}.pdf"
            )

            with open(filepath, "wb") as f:
                f.write(pdf_bytes)

            GENERATED_INCIDENTS.add(incident_id)

            logger.info(
                f"Auto-generated incident report: {filepath}"
            )

        except Exception as e:
            logger.error(
                f"Failed to auto-generate incident report: {e}"
            )


# ============================================================
# DUPLICATE EVENT DETECTOR
# ============================================================

from collections import OrderedDict


class DuplicateDetector:

    def __init__(self, max_size=10000):
        self.seen = OrderedDict()
        self.max_size = max_size

    def is_duplicate(self, event: dict) -> bool:

        host = event.get("host")
        record_id = event.get("event_record_id")

        if record_id is not None:
            key = (host, record_id)

        else:
            key = (
                host,
                event.get("event_id"),
                event.get("timestamp")
            )

            if not all(key):
                key = hash(
                    frozenset(
                        (
                            k,
                            str(v)
                        )
                        for k, v in event.items()
                        if k not in (
                            "raw_json",
                            "id",
                            "created_at"
                        )
                    )
                )

        if key in self.seen:
            return True

        self.seen[key] = True

        if len(self.seen) > self.max_size:
            self.seen.popitem(last=False)

        return False


DUPLICATE_DETECTOR = DuplicateDetector()


# ============================================================
# MAIN EVENT PROCESSING
# ============================================================

async def process_event(
    event: dict,
    engine: SigmaEngine,
    correlator: AlertCorrelator,
    mapper: MitreMapper
):

    # --------------------------------------------------------
    # Duplicate check
    # --------------------------------------------------------

    if DUPLICATE_DETECTOR.is_duplicate(event):

        logger.info(
            "Duplicate event ignored: "
            f"{event.get('event_record_id') or event.get('event_id')}"
        )

        return

    logger.info(
        f"Processing event: "
        f"{event.get('event_id')} "
        f"from {event.get('host')}"
    )

    # --------------------------------------------------------
    # Sigma detection
    # --------------------------------------------------------

    matches = engine.match_event(event)

    if not matches:

        logger.info(
            "Event did not match any Sigma rule."
        )

        return

    logger.warning(
        f"Event matched {len(matches)} Sigma rules!"
    )

    # --------------------------------------------------------
    # Send event to backend
    # --------------------------------------------------------

    async with httpx.AsyncClient() as client:

        try:

            evt_resp = await client.post(
                f"{BACKEND_API_URL}/events/",
                json=event
            )

            if evt_resp.status_code != 201:

                logger.error(
                    f"Failed to create event: "
                    f"{evt_resp.text}"
                )

                return

            event_uuid = evt_resp.json().get("event_id")

            if not event_uuid:

                logger.error(
                    "Backend did not return event_id, "
                    "aborting alert creation."
                )

                return

            logger.info(
                f"Backend event created: {event_uuid}"
            )

        except Exception as e:

            logger.error(
                f"Error communicating with backend "
                f"(events): {e}"
            )

            return

        # ----------------------------------------------------
        # Create alerts for every Sigma match
        # ----------------------------------------------------

        for match in matches:

            mitre_info = (
                mapper.get_technique_details(
                    match["technique_id"]
                )
                or {}
            )

            alert_payload = {

                "rule_name":
                    match["rule_name"],

                "severity":
                    match["severity"],

                "technique_id":
                    match["technique_id"],

                "technique_name":
                    mitre_info.get("name"),

                "tactic":
                    mitre_info.get("tactic"),

                "event_id":
                    event_uuid
            }

            # ------------------------------------------------
            # Correlation
            # ------------------------------------------------

            incident_id = correlator.correlate_alert(
                alert_payload,
                event
            )

            alert_payload["incident_id"] = incident_id

            try:

                # --------------------------------------------
                # Create alert
                # --------------------------------------------

                alt_resp = await client.post(
                    f"{BACKEND_API_URL}/alerts/",
                    json=alert_payload
                )

                if alt_resp.status_code != 201:

                    logger.error(
                        f"Failed to create alert: "
                        f"{alt_resp.text}"
                    )

                    continue

                alert_uuid = alt_resp.json().get(
                    "alert_id"
                )

                logger.info(
                    f"Created alert {alert_uuid} "
                    f"for rule {match['rule_name']}"
                )

                # --------------------------------------------
                # AI triage
                # --------------------------------------------

                logger.info(
                    "Requesting AI triage explanation..."
                )

                ai_result = await get_ai_explanation(
                    alert_payload,
                    event
                )

                ai_payload = {

                    "ai_explanation":
                        ai_result["explanation"],

                    "ai_recommendations":
                        ai_result["recommendations"]
                }

                ai_resp = await client.patch(
                    f"{BACKEND_API_URL}/alerts/"
                    f"{alert_uuid}/ai",
                    json=ai_payload
                )

                if ai_resp.status_code == 200:

                    logger.info(
                        f"Successfully updated alert "
                        f"{alert_uuid} with AI triage."
                    )

                    alert_payload[
                        "ai_explanation"
                    ] = ai_result["explanation"]

                    alert_payload[
                        "ai_recommendations"
                    ] = ai_result["recommendations"]

                else:

                    logger.error(
                        f"Failed to update AI triage: "
                        f"{ai_resp.text}"
                    )

                # --------------------------------------------
                # Incident report
                # --------------------------------------------

                maybe_generate_incident_report(
                    incident_id,
                    correlator
                )

            except Exception as e:

                logger.error(
                    f"Error processing alert pipeline: {e}"
                )


# ============================================================
# CONTROLLED LSASS INTEGRATION TEST
# ============================================================

async def run_lsass_test(
    engine: SigmaEngine,
    correlator: AlertCorrelator,
    mapper: MitreMapper
):

    logger.info("=" * 70)
    logger.info("CONTROLLED LSASS INTEGRATION TEST")
    logger.info("=" * 70)

    # --------------------------------------------------------
    # Controlled Event ID 10 fixture
    #
    # This does NOT access the real LSASS process.
    # It represents the normalized structure that the
    # Sysmon listener would normally provide.
    # --------------------------------------------------------

    test_event = {

        "event_id": 10,

        "host": "EDR-TEST",

        "timestamp":
            "2026-08-10T00:00:00Z",

        "event_record_id":
            "LSASS-TEST-001",

        # Fields used by the LSASS Sigma rule

        "source_image":
            r"C:\EDR-Test\test-process.exe",

        "target_image":
            r"C:\Windows\System32\lsass.exe",

        "granted_access":
            "0x1410",

        "call_trace":
            "",

        # Other normalized fields

        "process_name":
            r"C:\EDR-Test\test-process.exe",

        "parent_process":
            None,

        "command_line":
            None,

        "parent_command_line":
            None,

        "target_object":
            None,

        "target_filename":
            None,

        "dest_ip":
            None,

        "dest_port":
            None,

        "query_name":
            None,

        "user":
            "EDR-Test"
    }

    logger.info("Test event created:")
    logger.info(
        f"  Event ID       : "
        f"{test_event['event_id']}"
    )

    logger.info(
        f"  Source Image   : "
        f"{test_event['source_image']}"
    )

    logger.info(
        f"  Target Image   : "
        f"{test_event['target_image']}"
    )

    logger.info(
        f"  Granted Access : "
        f"{test_event['granted_access']}"
    )

    logger.info("-" * 70)

    # --------------------------------------------------------
    # Send through the REAL process_event pipeline
    # --------------------------------------------------------

    await process_event(
        test_event,
        engine,
        correlator,
        mapper
    )

    logger.info("-" * 70)
    logger.info("CONTROLLED LSASS TEST FINISHED")
    logger.info("=" * 70)


# ============================================================
# MAIN
# ============================================================

async def main():

    logger.info(
        "Starting SOC-EDR Detection Engine..."
    )

    # --------------------------------------------------------
    # Load MITRE data
    # --------------------------------------------------------

    load_mitre_data()

    # --------------------------------------------------------
    # Load Sigma rules
    # --------------------------------------------------------

    rules = load_sigma_rules()

    from mitre.loader import (
        backfill_missing_techniques
    )

    backfill_missing_techniques(rules)

    if not rules:

        logger.warning(
            "No Sigma rules loaded. "
            "Engine will not detect anything."
        )

    # --------------------------------------------------------
    # Initialize detection components
    # --------------------------------------------------------

    engine = SigmaEngine(rules)

    correlator = AlertCorrelator()

    mapper = MitreMapper()

    # --------------------------------------------------------
    # CONTROLLED LSASS TEST MODE
    # --------------------------------------------------------

    if "--test-lsass" in sys.argv:

        logger.info(
            "LSASS test mode enabled."
        )

        await run_lsass_test(
            engine,
            correlator,
            mapper
        )

        return

    # --------------------------------------------------------
    # NORMAL SYSMON MODE
    # --------------------------------------------------------

    main_loop = asyncio.get_running_loop()

    def event_callback(normalized_event):

        asyncio.run_coroutine_threadsafe(
            process_event(
                normalized_event,
                engine,
                correlator,
                mapper
            ),
            main_loop
        )

    logger.info(
        "Starting Sysmon listener..."
    )

    await listen_async(event_callback)


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        asyncio.run(main())

    except KeyboardInterrupt:

        logger.info(
            "Detection Engine stopped by user."
        )