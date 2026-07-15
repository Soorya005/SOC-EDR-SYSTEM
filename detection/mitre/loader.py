import sqlite3
import logging
import os
from config import PROJECT_ROOT

logger = logging.getLogger(__name__)

COMMON_TECHNIQUES = [
    {"technique_id": "T1059.001", "name": "PowerShell", "tactic": "Execution",
     "description": "Adversaries may abuse PowerShell commands and scripts for execution."},
    {"technique_id": "T1055", "name": "Process Injection", "tactic": "Defense Evasion, Privilege Escalation",
     "description": "Adversaries may inject code into processes to evade defenses or elevate privileges."},
    {"technique_id": "T1003.001", "name": "LSASS Memory", "tactic": "Credential Access",
     "description": "Adversaries may access credential material stored in LSASS process memory."},
    {"technique_id": "T1547.001", "name": "Registry Run Keys / Startup Folder", "tactic": "Persistence",
     "description": "Adversaries may achieve persistence by adding a program to a startup folder or Registry run key."},
    {"technique_id": "T1112", "name": "Modify Registry", "tactic": "Defense Evasion",
     "description": "Adversaries may interact with the Windows Registry to hide configuration or evade defenses."},
    {"technique_id": "T1047", "name": "Windows Management Instrumentation", "tactic": "Execution",
     "description": "Adversaries may abuse WMI to execute malicious commands and payloads."},
    {"technique_id": "T1071.004", "name": "DNS", "tactic": "Command and Control",
     "description": "Adversaries may use DNS traffic to communicate with C2 infrastructure."},
    {"technique_id": "T1105", "name": "Ingress Tool Transfer", "tactic": "Command and Control",
     "description": "Adversaries may transfer tools or files onto a compromised host."},
    {"technique_id": "T1204.002", "name": "Malicious File", "tactic": "Execution",
     "description": "Adversaries may rely on a user opening a malicious file to gain execution."},
    {"technique_id": "T1027", "name": "Obfuscated Files or Information", "tactic": "Defense Evasion",
     "description": "Adversaries may encode/encrypt data to make content difficult to detect."},
    {"technique_id": "T1053.005", "name": "Scheduled Task", "tactic": "Persistence, Privilege Escalation, Execution",
     "description": "Adversaries may abuse Windows Task Scheduler to execute malicious code."},
    {"technique_id": "T1070.001", "name": "Clear Windows Event Logs", "tactic": "Defense Evasion",
     "description": "Adversaries may clear event logs to hide evidence of an intrusion."},
]


def load_mitre_data():
    db_path = PROJECT_ROOT / "backend" / "database" / "edr.db"

    if not os.path.exists(db_path):
        logger.error(f"Database not found at {db_path}. Run backend first.")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        for t in COMMON_TECHNIQUES:
            cursor.execute("""
                INSERT OR IGNORE INTO mitre_techniques (technique_id, name, tactic, description)
                VALUES (?, ?, ?, ?)
            """, (t['technique_id'], t['name'], t['tactic'], t['description']))

        conn.commit()
        conn.close()
        logger.info(f"Loaded {len(COMMON_TECHNIQUES)} MITRE techniques into database.")
    except Exception as e:
        logger.error(f"Failed to load MITRE data into DB: {e}")


def backfill_missing_techniques(rules: list):
    """
    Scans loaded Sigma rules for attack.t* tags not present in COMMON_TECHNIQUES,
    inserts a stub row so mapper.get_technique_details() never returns None for a real match.
    Call this after load_sigma_rules(), passing the rules list, in main.py.
    """
    db_path = PROJECT_ROOT / "backend" / "database" / "edr.db"
    if not os.path.exists(db_path):
        return

    known_ids = {t["technique_id"].lower() for t in COMMON_TECHNIQUES}
    found_ids = set()

    for rule in rules:
        for tag in rule.get("tags", []):
            if tag.startswith("attack.t"):
                tid = tag.replace("attack.", "").upper()
                if tid.lower() not in known_ids:
                    found_ids.add(tid)

    if not found_ids:
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        for tid in found_ids:
            cursor.execute("""
                INSERT OR IGNORE INTO mitre_techniques (technique_id, name, tactic, description)
                VALUES (?, ?, ?, ?)
            """, (tid, tid, "Unknown", "Technique referenced by loaded Sigma rule; details not yet catalogued."))
        conn.commit()
        conn.close()
        logger.info(f"Backfilled {len(found_ids)} unrecognized technique IDs.")
    except Exception as e:
        logger.error(f"Failed to backfill techniques: {e}")