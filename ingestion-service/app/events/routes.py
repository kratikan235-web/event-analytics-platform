from fastapi import APIRouter, status
from app.events.schemas import EventCreate
from app.kafka.producer import send_event
from app.core.kafka_config import KAFKA_TOPIC
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/events", tags=["events"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate):

    logger.info("Event received")

    event_data = event.model_dump(mode="json")

    try:
      # Send event to Kafka
      send_event(KAFKA_TOPIC, event_data)

      logger.info("Event sent to Kafka successfully")
    
    except Exception as e:
        logger.exception("Failed to send event to Kafka")
        raise HTTPException(status_code=500, detail="Kafka publish failed")

    return {
        "message": "Event received and sent to Kafka",
        "event": event_data,

    }
