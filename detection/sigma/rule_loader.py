import os
import yaml
import logging
from config import SIGMA_RULES_DIR

logger = logging.getLogger(__name__)

def load_sigma_rules():
    """
    Loads all Sigma rules (.yml, .yaml) from the stable and custom directories.
    Returns a list of parsed Python dictionaries representing the rules.
    """
    rules = []
    
    directories = [
        SIGMA_RULES_DIR / "stable",
        SIGMA_RULES_DIR / "custom"
    ]
    
    for directory in directories:
        if not directory.exists():
            logger.warning(f"Sigma rules directory not found: {directory}")
            continue
            
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.yml') or file.endswith('.yaml'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            # Sigma rules can sometimes contain multiple documents, but usually it's just one
                            docs = yaml.safe_load_all(f)
                            for doc in docs:
                                if doc and 'detection' in doc:
                                    rules.append(doc)
                    except Exception as e:
                        logger.error(f"Failed to load Sigma rule {file_path}: {e}")
                        
    logger.info(f"Loaded {len(rules)} Sigma rules.")
    return rules
