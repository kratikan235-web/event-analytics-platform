from fastapi import APIRouter
from app.events.schemas import EventCreate

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/")
async def ingest_event(event: EventCreate):
    # Later: call service layer (Kafka)
    return {
        "message": "Event received",
        "event_type": event.event_type,
        "user_id": event.user_id
    }