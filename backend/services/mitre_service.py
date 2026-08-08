from database import repositories

def get_mitre_techniques():
    """
    Fetches the MITRE ATT&CK techniques report from database repository.
    """
    return repositories.get_mitre_techniques_report()
