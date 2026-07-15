import sqlite3
import logging
import os
from config import PROJECT_ROOT

logger = logging.getLogger(__name__)

class MitreMapper:
    def __init__(self):
        self.db_path = PROJECT_ROOT / "backend" / "database" / "edr.db"
        
    def get_technique_details(self, technique_id):
        """
        Retrieves MITRE technique details from the database by ID.
        """
        if not technique_id:
            return None
            
        if not os.path.exists(self.db_path):
            return None
            
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM mitre_techniques WHERE technique_id = ?",
                (technique_id,)
            )
            row = cursor.fetchone()
            conn.close()
            
            if row:
                return dict(row)
        except Exception as e:
            logger.error(f"Error mapping technique {technique_id}: {e}")
            
        return None
