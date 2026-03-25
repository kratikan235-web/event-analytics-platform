FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y default-jdk

COPY spark_processing/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY common-logging /common-logging
RUN pip install /common-logging

# COPY FULL STRUCTURE
COPY spark_processing /app

ENV PYTHONPATH=/app

# UPDATED PATH
CMD ["python", "app/processing/spark_processor.py"]