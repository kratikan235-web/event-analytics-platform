import os
import shutil
from pyspark.sql import SparkSession
from pyspark.sql.functions import current_timestamp

from app.schemas.event_schema import ProcessedEvent
from app.db.database import SessionLocal
from app.db.models import Event
from dotenv import load_dotenv
import os
import logging
from common_logging.logging_config import setup_logging

logging.getLogger("py4j").setLevel(logging.ERROR)

setup_logging("spark_processor")
logger = logging.getLogger(__name__)

load_dotenv()

# RAW_PATH = os.getenv("RAW_PATH")
# PROCESSED_PATH = os.getenv("PROCESSED_PATH")
if os.getenv("DOCKER_ENV") == "true":
    RAW_PATH = "/app/raw_events"
    PROCESSED_PATH = "/app/processed_events"
else:
    RAW_PATH = "/home/kratika/Documents/Projects/event-analytics-platform/consumer-service/raw_events/"
    PROCESSED_PATH = "/home/kratika/Documents/Projects/event-analytics-platform/consumer-service/processed_events/"

def create_spark_session():
    logger.info("Creating Spark session")

    os.environ["SPARK_LOCAL_IP"] = "127.0.0.1"

    spark = (
        SparkSession.builder
        .appName("EventProcessingJob")
        .config("spark.sql.session.timeZone", "UTC")
        .config("spark.ui.showConsoleProgress", "false")
        .config("spark.ui.enabled", "false")
        .getOrCreate()
    )

    # Reduce Spark internal logs
    spark.sparkContext.setLogLevel("ERROR")

    return spark

def read_events(spark):
    logger.info(f"Reading events from {RAW_PATH}")
    # return spark.read.json(RAW_PATH)
    # return spark.read.json(f"{RAW_PATH}/**/*.json")
    return spark.read.option("recursiveFileLookup", "true").json(RAW_PATH)

def transform_events(df):
    logger.info("Transforming events")
    df = df.withColumn("processed_at", current_timestamp())

    columns = df.columns

    select_cols = ["event_type", "user_id", "timestamp", "processed_at"]

    if "payload" in columns:
        select_cols.insert(2, "payload")

    df = df.select(*select_cols)

    dedupe_cols = ["event_type", "user_id", "timestamp"]

    if "payload" in df.columns:
        dedupe_cols.append("payload")
 
    df = df.dropDuplicates(dedupe_cols)
    logger.info("Deduplication completed")
    return df

def validate_events(rows):
    logger.info("Validating events")
    validated = []

    for row in rows:
        data = row.asDict()

        if "payload" in data and data["payload"] is not None:
            data["payload"] = data["payload"].asDict()
        else:
            data["payload"] = None
        validated.append(ProcessedEvent(**data))
    logger.info(f"Validation completed. Validated {len(validated)} events.")
    return validated


def save_events(events):
    logger.info(f"Saving {len(events)} events to database")
    db = SessionLocal()

    db.add_all([
        Event(
            event_type=e.event_type,
            user_id=e.user_id,
            payload=e.payload,
            event_timestamp=e.timestamp
        )
        for e in events
    ])

    db.commit()
    db.close()
    logger.info("Events saved to database successfully")

def move_files():
    moved = False

    for root, dirs, files in os.walk(RAW_PATH):
        for file in files:
            if not file.endswith(".json"):
                continue

            src = os.path.join(root, file)

            relative = os.path.relpath(root, RAW_PATH)
            dest_dir = os.path.join(PROCESSED_PATH, relative)

            os.makedirs(dest_dir, exist_ok=True)

            dest = os.path.join(dest_dir, file)
            shutil.move(src, dest)

            moved = True

    if moved:
        logger.info("Files moved to processed folder")

    # REMOVE EMPTY DIRECTORIES
    for root, dirs, files in os.walk(RAW_PATH, topdown=False):
        if not dirs and not files:
            os.rmdir(root)


def has_files(path):
    return any(
        file.endswith(".json")
        for _, _, files in os.walk(path)
        for file in files
    )

import time

def main():
    while True:
        try:
            if not os.path.exists(RAW_PATH):
                logger.info("RAW_PATH does not exist. Retrying...")
                time.sleep(5)
                continue

            if not has_files(RAW_PATH):
                logger.info("No files to process. Waiting...")
                time.sleep(5)   # wait instead of exit
                continue

            logger.info("Files found. Starting processing...")

            spark = create_spark_session()

            df = read_events(spark)

            logger.debug("printing raw dataframe schema")
            df.printSchema()

            logger.debug("showing raw dataframe sample data")
            df.show()

            processed_df = transform_events(df)

            rows = processed_df.toLocalIterator()

            events = validate_events(rows)

            save_events(events)

            move_files()

            spark.catalog.clearCache()
            spark.stop()

            logger.info("Processing completed successfully")

            time.sleep(5)  # avoid tight loop

        except Exception as e:
            logger.error(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()


