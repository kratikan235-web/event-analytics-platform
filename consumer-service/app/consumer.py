import json
import os
from kafka import KafkaConsumer
from dotenv import load_dotenv

from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

from app.db.database import SessionLocal
from app.db.models import Event
from app.raw_events import save_raw_event

load_dotenv()

consumer = KafkaConsumer(
    os.getenv("KAFKA_TOPIC"),
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    auto_offset_reset="earliest",
    enable_auto_commit=False,
    group_id=os.getenv("KAFKA_CONSUMER_GROUP"),
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

print("Consumer started. Waiting for events...")

for message in consumer:
    event_data = message.value
    db = SessionLocal()

    try:
        # Save raw event
        save_raw_event(event_data)

        # Save to PostgreSQL DB (Still raw for now)
        event = Event(
            event_type=event_data["event_type"],
            user_id=event_data.get("user_id"),
            event_timestamp=datetime.utcnow(),
            payload=event_data.get("payload"),
        )

        db.add(event)
        db.commit()        # DB success
        consumer.commit()  # Kafka offset commit AFTER DB

        print("Event saved to DB:", event_data)

    except SQLAlchemyError as e:
        db.rollback()
        print("DB error:", e)

    except Exception as e:
        print("Unexpected error:", e)

    finally:
        db.close()