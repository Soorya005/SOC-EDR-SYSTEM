import httpx
import logging
from config import OLLAMA_API_URL, OLLAMA_MODEL
from ai_triage.prompt_templates import ALERT_TRIAGE_PROMPT

logger = logging.getLogger(__name__)

async def get_ai_explanation(alert_data: dict, event_data: dict) -> dict:
    """
    Sends alert and event context to the local Ollama LLM to get an explanation and recommendations.
    Returns a dict with 'explanation' and 'recommendations'.
    """
    prompt = ALERT_TRIAGE_PROMPT.format(
        rule_name=alert_data.get('rule_name', 'Unknown'),
        severity=alert_data.get('severity', 'Medium'),
        technique_id=alert_data.get('technique_id', 'Unknown'),
        host=event_data.get('host', 'Unknown'),
        process_name=event_data.get('process_name', 'Unknown'),
        parent_process=event_data.get('parent_process', 'Unknown'),
        command_line=event_data.get('command_line', 'Unknown')
    )
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    result = {
        "explanation": "AI analysis failed.",
        "recommendations": "Investigate manually."
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OLLAMA_API_URL}/api/generate",
                json=payload,
                timeout=180.0  # 3 minutes — Mistral needs time on first load
            )
            
            if response.status_code == 200:
                resp_json = response.json()
                text = resp_json.get('response', '')
                
                # Parse out the explanation and recommendations sections
                if "EXPLANATION:" in text and "RECOMMENDATIONS:" in text:
                    parts = text.split("RECOMMENDATIONS:")
                    explanation_part = parts[0].replace("EXPLANATION:", "").strip()
                    recs_part = parts[1].strip()
                    
                    result["explanation"] = explanation_part
                    result["recommendations"] = recs_part
                else:
                    result["explanation"] = text
                    result["recommendations"] = "See explanation."
            else:
                logger.error(f"Ollama API returned status {response.status_code}")
                
    except Exception as e:
        logger.error(f"Failed to connect to Ollama: {e}")
        
    return result
