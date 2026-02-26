import json
import os
from kafka import KafkaConsumer
from dotenv import load_dotenv

load_dotenv()

consumer = KafkaConsumer(
    os.getenv("KAFKA_TOPIC"),
    bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id=os.getenv("KAFKA_CONSUMER_GROUP"),
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
)

print("Consumer started. Waiting for events...")

for message in consumer:
    event = message.value
    print("Event received:", event)