import json
from confluent_kafka import Producer
from app.core.kafka_config import KAFKA_BOOTSTRAP_SERVERS

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(
            f"Event delivered to {msg.topic()} "
            f"[partition {msg.partition()}]"
        )


producer = Producer(
    {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
    }
)


def send_event(topic: str, event: dict):
    producer.produce(
        topic=topic,
        value=json.dumps(event),
        callback=delivery_report,
    )
    producer.flush()