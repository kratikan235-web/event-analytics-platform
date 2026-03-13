from fastapi import FastAPI
from app.api.analytics import router as analytics_router
from common_logging.logging_config import setup_logging

setup_logging("analytics-service")

app = FastAPI(title="Analytics Service")

app.include_router(analytics_router, prefix="/analytics")