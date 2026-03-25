import json
import time
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


producer = None


def get_producer():
    global producer

    if producer is not None:
        return producer

    for i in range(10):
        try:
            print(f"Connecting to Kafka... attempt {i+1}")
            producer = Producer({
                "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS
            })
            print("Kafka connected")
            return producer
        except Exception as e:
            print(f"Kafka not ready: {e}")
            time.sleep(5)

    raise Exception("Kafka connection failed after retries")


def send_event(topic: str, event: dict):
    p = get_producer()

    p.produce(
        topic=topic,
        value=json.dumps(event),
        callback=delivery_report,
    )
    p.poll(0)
