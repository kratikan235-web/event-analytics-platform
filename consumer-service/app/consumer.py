import json
import os
from kafka import KafkaConsumer
from dotenv import load_dotenv

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

    try:
        # Save raw event
        save_raw_event(event_data)
        print(f"Raw event saved: {event_data}")

        consumer.commit()

    except Exception as e:
        print("Error saving raw event:", e)
