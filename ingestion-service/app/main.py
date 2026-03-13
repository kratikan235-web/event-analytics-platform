from fastapi import FastAPI
from app.events.routes import router as events_router
import logging
from common_logging.logging_config import setup_logging

setup_logging("ingestion")

logger = logging.getLogger(__name__)

app = FastAPI(title="Event Ingestion Service")

app.include_router(events_router)