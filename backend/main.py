from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import initialize_database
from api import events
from api import alerts
from api import stats
from api import reports
from api import mitre
from api.incidents import router as incidents_router

# Create database tables
initialize_database()

app = FastAPI(
    title="SOC EDR Backend",
    version="1.0.0",
    description="AI Assisted EDR Investigation Platform"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # We'll restrict this later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(events.router)
app.include_router(alerts.router)
app.include_router(stats.router)
app.include_router(reports.router)
app.include_router(incidents_router)
app.include_router(mitre.router)
from database.db import get_connection

@app.get("/health", tags=["Health"])
def health():
    try:
        conn = get_connection()
        conn.execute("SELECT 1")
        conn.close()

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }
@app.get("/")
def root():
    return {
        "message": "SOC EDR Backend Running"
    }

