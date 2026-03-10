import os
import shutil
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

from app.schemas.event_schema import ProcessedEvent
from app.db.database import SessionLocal
from app.db.models import Event
from dotenv import load_dotenv
import os

load_dotenv()

RAW_PATH = os.getenv("RAW_PATH")
PROCESSED_PATH = os.getenv("PROCESSED_PATH")

def create_spark_session():
    return SparkSession.builder.appName("EventProcessingJob").getOrCreate()


def read_events(spark):
    return spark.read.json(RAW_PATH)


def transform_events(df):

    df = df.withColumn("processed_at", current_timestamp())

    columns = df.columns

    select_cols = ["event_type", "user_id", "timestamp", "processed_at"]

    if "payload" in columns:
        select_cols.insert(2, "payload")

    df = df.select(*select_cols)

    dedupe_cols = ["event_type", "user_id", "timestamp"]

    if "payload" in df.columns:
        dedupe_cols.append("payload")

    return df.dropDuplicates(dedupe_cols)

def validate_events(rows):
    validated = []

    for row in rows:
        data = row.asDict()

        if "payload" in data and data["payload"] is not None:
            data["payload"] = data["payload"].asDict()
        else:
            data["payload"] = None
        validated.append(ProcessedEvent(**data))
    return validated


def save_events(events):
    db = SessionLocal()

    db.add_all([
        Event(
            event_type=e.event_type,
            user_id=e.user_id,
            payload=e.payload,
            event_timestamp=e.processed_at
        )
        for e in events
    ])

    db.commit()
    db.close()


def move_files():
    os.makedirs(PROCESSED_PATH, exist_ok=True)

    for file in os.listdir(RAW_PATH):
        shutil.move(
            os.path.join(RAW_PATH, file),
            os.path.join(PROCESSED_PATH, file)
        )

def main():
    if not os.listdir(RAW_PATH):
        print("No raw events to process.")
        return

    spark = create_spark_session()

    df = read_events(spark)

    # DEBUG
    df.printSchema()
    df.show()

    processed_df = transform_events(df)

    rows = processed_df.toLocalIterator()

    events = validate_events(rows)

    save_events(events)

    move_files()


if __name__ == "__main__":
    main()