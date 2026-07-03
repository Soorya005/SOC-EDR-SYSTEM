CREATE TABLE IF NOT EXISTS mitre_techniques (
    technique_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    tactic TEXT NOT NULL,
    description TEXT
);

-- sysmon events
CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    event_id INTEGER NOT NULL,
    host TEXT,
    process_name TEXT,
    parent_process TEXT,
    command_line TEXT,
    raw_json TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS alerts (
    id TEXT PRIMARY KEY,
    rule_name TEXT NOT NULL,
    severity TEXT NOT NULL DEFAULT 'Medium',
    status TEXT NOT NULL DEFAULT 'New',

    technique_id TEXT,
    event_id TEXT,

    incident_id TEXT,

    ai_explanation TEXT,
    ai_recommendations TEXT,

    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),

    

    FOREIGN KEY (event_id)
REFERENCES events(id)
ON DELETE CASCADE 
);


CREATE TABLE IF NOT EXISTS investigations (
    id TEXT PRIMARY KEY,
    alert_id TEXT NOT NULL,
    analyst_notes TEXT NOT NULL,

    created_at TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at TEXT NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (alert_id)
        REFERENCES alerts(id)
);