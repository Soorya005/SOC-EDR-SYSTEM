from database import repositories


def get_summary():
    """
    Return dashboard summary statistics.
    """
    return repositories.get_summary_stats()


def get_trends():
    """
    Return daily alert trends.
    """
    return repositories.get_alert_trends()


def get_heatmap():
    """
    Return MITRE ATT&CK heatmap data.
    """
    return repositories.get_heatmap_data()
