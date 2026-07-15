import win32evtlog
import win32event
import win32con
import win32evtlogutil
import time
import logging
import asyncio
from sysmon.normalizer import parse_sysmon_xml
from config import SYSMON_CHANNEL

logger = logging.getLogger(__name__)

def listen_for_events(callback=None):
    """
    Subscribes to the Windows Sysmon event log and captures real-time events.
    For each event, it fetches the XML representation, normalizes it,
    and passes the normalized dict to the callback function.
    """
    server = 'localhost'
    log_type = SYSMON_CHANNEL
    
    try:
        # Open the event log
        hand = win32evtlog.OpenEventLog(server, log_type)
        flags = win32evtlog.EVENTLOG_FORWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        
        # Seek to the end (we only want new events)
        # Note: In a real production environment, you might want to track the last record number
        # so you don't miss events if the service stops. For this basic implementation, we just read forward.
        total_records = win32evtlog.GetNumberOfEventLogRecords(hand)
        
        logger.info(f"Listening for Sysmon events on {log_type}. Total records so far: {total_records}")

        while True:
            events = win32evtlog.ReadEventLog(hand, flags, 0)
            
            if not events:
                # No new events, sleep briefly
                time.sleep(1)
                continue
                
            for event in events:
                # To get the XML, we can use the Evt API via win32evtlog
                # Unfortunately, standard ReadEventLog gives strings, not full XML easily.
                # However, for Sysmon, win32evtlogutil might not give full XML natively.
                # Let's use EvtQuery and EvtNext for modern XML event logs.
                pass
                
    except Exception as e:
        logger.error(f"Failed to listen to event log: {e}")

# Modern approach using Evt API (Windows Vista+ Event Log API) which gives XML
def listen_for_events_modern(callback):
    """
    Listens to modern Event Log (XML) for Sysmon events.
    """
    import win32evtlog
    
    channel = SYSMON_CHANNEL
    query = "*"
    
    # Subscribe to future events
    flags = win32evtlog.EvtSubscribeToFutureEvents
    
    def on_event(action, context, event_handle):
        if action == win32evtlog.EvtSubscribeActionDeliver:
            try:
                # Render the event to XML
                xml_content = win32evtlog.EvtRender(event_handle, win32evtlog.EvtRenderEventXml)
                
                # Normalize the XML
                normalized_event = parse_sysmon_xml(xml_content)
                
                # We only care about events with an ID
                if normalized_event.get("event_id") is not None:
                    if callback:
                        # If callback is async, we would need a different handling,
                        # but we can schedule it on the loop.
                        callback(normalized_event)
                        
            except Exception as e:
                logger.error(f"Error processing event: {e}")
                
        return 0

    try:
        # Subscribe
        subscription = win32evtlog.EvtSubscribe(
            channel, 
            flags, 
            None, 
            Callback=on_event,
            Query=query
        )
        logger.info(f"Subscribed to {channel}")
        
        # Keep the main thread alive while background threads handle callbacks
        while True:
            time.sleep(1)
            
    except Exception as e:
        logger.error(f"Subscription failed: {e}")

async def listen_async(callback):
    """
    Async wrapper for modern event listening, running in an executor.
    """
    loop = asyncio.get_event_loop()
    # Run the blocking modern listener in a separate thread
    await loop.run_in_executor(None, listen_for_events_modern, callback)
