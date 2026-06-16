from fastapi import FastAPI

from backend.api import alerts, events, reports, stats

app = FastAPI(title="SOC EDR System")

app.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
app.include_router(events.router, prefix="/events", tags=["events"])
app.include_router(stats.router, prefix="/stats", tags=["stats"])
app.include_router(reports.router, prefix="/reports", tags=["reports"])


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}