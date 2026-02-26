from fastapi import FastAPI
from app.events.routes import router as events_router

app = FastAPI(title="Event Ingestion Service")

app.include_router(events_router)