ALERT_TRIAGE_PROMPT = """You are an expert Security Operations Center (SOC) analyst.
Analyze the following security alert and provide a structured explanation and recommendation.

Alert Details:
- Rule Name: {rule_name}
- Severity: {severity}
- MITRE Technique: {technique_id}

Event Context:
- Host: {host}
- Process Name: {process_name}
- Parent Process: {parent_process}
- Command Line: {command_line}

Based on this information, provide:
1. EXPLANATION: A brief (2-3 sentences) explanation of why this activity is suspicious or malicious.
2. RECOMMENDATIONS: Bullet points of 2-3 concrete investigation or remediation steps the analyst should take next.

Format your response exactly like this:
EXPLANATION: <your explanation>
RECOMMENDATIONS: <your recommendations>
"""