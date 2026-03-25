FROM python:3.12-slim

WORKDIR /app

COPY consumer-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY common-logging /common-logging
RUN pip install /common-logging

COPY consumer-service /app

CMD ["python", "-m", "app.consumer"]