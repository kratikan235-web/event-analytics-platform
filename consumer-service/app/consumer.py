import json
import os
from kafka import KafkaConsumer
from dotenv import load_dotenv
from app.raw_events import save_raw_event
import logging
from common_logging.logging_config import setup_logging

load_dotenv()

setup_logging("consumer")
logger = logging.getLogger(__name__)
logging.getLogger("kafka").setLevel(logging.WARNING)
import time

while True:
    try:
        logger.info("Connecting to Kafka...")

        consumer = KafkaConsumer(
            os.getenv("KAFKA_TOPIC"),
            bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
            auto_offset_reset="latest",
            enable_auto_commit=True,
            group_id=os.getenv("KAFKA_CONSUMER_GROUP"),
            value_deserializer=lambda x: json.loads(x.decode("utf-8")),
        )

        logger.info("Consumer started. Waiting for events...")
        break

    except Exception as e:
        logger.error(f"Kafka not ready, retrying... {e}")
        time.sleep(5)

for message in consumer:
    event_data = message.value

    try:
        # Save raw event
        save_raw_event(event_data)
        logger.info(f"Raw event saved: {event_data}")

        consumer.commit()

    except Exception as e:
        logger.exception("Error saving raw event")

