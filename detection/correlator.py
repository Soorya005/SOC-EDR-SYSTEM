
import logging
import uuid
import time

logger = logging.getLogger(__name__)

class AlertCorrelator:
    def __init__(self, time_window_seconds=300):
        """
        A simple alert correlator that groups alerts into incidents 
        if they occur on the same host within the time window.
        """
        self.time_window = time_window_seconds
        self.active_incidents = {}  # host -> {"incident_id": str, "last_updated": float, "alerts": []}
        
    def correlate_alert(self, alert_data: dict, event_data: dict) -> str:
        """
        Takes an alert and its corresponding event data, and returns an incident_id.
        If the alert is part of an active incident on the same host, it returns the existing ID.
        Otherwise, it creates a new incident ID.
        """
        host = event_data.get("host")
        if not host:
            return str(uuid.uuid4())
            
        current_time = time.time()
        
        if host in self.active_incidents:
            incident = self.active_incidents[host]
            # Check if incident is still active (within time window)
            if current_time - incident["last_updated"] <= self.time_window:
                # Update last updated time and return existing ID
                incident["last_updated"] = current_time
                incident["alerts"].append(alert_data)
                logger.info(f"Correlated alert to existing incident {incident['incident_id']} for host {host}")
                return incident["incident_id"]
            else:
                logger.info(f"Incident {incident['incident_id']} expired for host {host}, starting new one.")
                
        # Create new incident
        new_incident_id = str(uuid.uuid4())

        # Keep it in memory for correlation
        self.active_incidents[host] = {
            "incident_id": new_incident_id,
            "last_updated": current_time,
            "alerts": [alert_data]
        }

        logger.info(f"Created new incident {new_incident_id} for host {host}")

        return new_incident_id

        # Keep it in memory for correlation
        self.active_incidents[host] = {
            "incident_id": new_incident_id,
            "last_updated": current_time,
            "alerts": [alert_data]
        }

        logger.info(f"Created new incident {new_incident_id} for host {host}")

        return new_incident_id

    def get_incident_alerts(self, incident_id: str) -> list:
        for incident in self.active_incidents.values():
            if incident["incident_id"] == incident_id:
                return incident["alerts"]
        return []