import xml.etree.ElementTree as ET
import logging

logger = logging.getLogger(__name__)

FIELD_MAP = {
    "Image": "process_name",
    "ParentImage": "parent_process",
    "CommandLine": "command_line",
    "ParentCommandLine": "parent_command_line",
    "TargetObject": "target_object",       # registry key (ID 12/13)
    "TargetImage": "target_image",         # process access target, e.g. lsass.exe (ID 10)
    "TargetFilename": "target_filename",   # file creation (ID 11)
    "DestinationIp": "dest_ip",            # network connection (ID 3)
    "DestinationPort": "dest_port",
    "QueryName": "query_name",             # DNS (ID 22)
    "SourceImage": "source_image",
    "ProcessGuid": "process_guid",
    "User": "user",
}


def parse_sysmon_xml(xml_string: str) -> dict:
    """
    Parses a raw Sysmon XML event into a normalized dictionary.
    Covers process creation, registry, file, network, DNS, and process access events.
    """
    normalized_event = {
        "event_id": None,
        "host": None,
        "timestamp": None,
    }
    for field in FIELD_MAP.values():
        normalized_event[field] = None

    try:
        root = ET.fromstring(xml_string)

        ns = ""
        if '}' in root.tag:
            ns = root.tag.split('}')[0] + '}'

        system = root.find(f'{ns}System')
        event_data = root.find(f'{ns}EventData')

        if system is not None:
            event_id_elem = system.find(f'{ns}EventID')
            if event_id_elem is not None and event_id_elem.text:
                normalized_event["event_id"] = int(event_id_elem.text)

            computer_elem = system.find(f'{ns}Computer')
            if computer_elem is not None and computer_elem.text:
                normalized_event["host"] = computer_elem.text

            time_elem = system.find(f'{ns}TimeCreated')
            if time_elem is not None:
                normalized_event["timestamp"] = time_elem.get("SystemTime")

        if event_data is not None:
            for data in event_data.findall(f'{ns}Data'):
                name = data.get("Name")
                text = data.text

                if not text or name not in FIELD_MAP:
                    continue

                normalized_event[FIELD_MAP[name]] = text

        return normalized_event

    except Exception as e:
        logger.error(f"Error parsing Sysmon XML: {e}")
        return normalized_event