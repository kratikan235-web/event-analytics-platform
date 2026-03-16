import os
import json
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def save_raw_event(event_data):
    now = datetime.utcnow()

    year = now.strftime("%Y")
    month = now.strftime("%m")
    day = now.strftime("%d")

    partition_path = os.path.join(
        BASE_DIR,
        "raw_events",
        f"year={year}",
        f"month={month}",
        f"day={day}"
    )

    os.makedirs(partition_path, exist_ok=True)
    timestamp = now.strftime("%Y%m%d_%H%M%S_%f")
    filename = os.path.join(partition_path, f"event_{timestamp}.json")


    with open(filename, "w") as f:
        json.dump(event_data, f)