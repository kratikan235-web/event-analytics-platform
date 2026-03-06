import os
import json
from datetime import datetime

def save_raw_event(event_data):
    os.makedirs("raw_events", exist_ok=True)
    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S_%f")
    filename = f"raw_events/event_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(event_data, f)