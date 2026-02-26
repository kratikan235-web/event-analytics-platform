from fastapi import APIRouter, status
from app.events.schemas import EventCreate
from app.kafka.producer import send_event
from app.core.kafka_config import EVENTS_TOPIC

router = APIRouter(prefix="/events", tags=["events"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate):
    event_data = event.model_dump(mode="json")

    # Send event to Kafka
    send_event(EVENTS_TOPIC, event_data)

    return {
        "message": "Event received and sent to Kafka",
        "event": event_data,

    }
