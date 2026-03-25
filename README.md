# Event Analytics Platform

An event-driven analytics backend built using FastAPI, Kafka, PostgreSQL, Redis, and Docker.
The system ingests events, processes them asynchronously, stores raw and cleaned data, and provides analytics APIs for querying insights.

# Architecture
Client
  ↓
FastAPI (Event Ingestion API)
  ↓
Kafka (Message Broker)
  ↓
Consumer Service
  ↓
Raw Data Storage (JSON / S3)
  ↓
Processing Layer (Spark)
  ↓
PostgreSQL (Clean Data)
  ↓
Analytics APIs
  ↓
Redis (Cache)

# Tech Stack
Python
FastAPI
Apache Kafka
PostgreSQL
Redis
Apache Spark
SQLAlchemy
Pydantic
Docker

# Features
Event ingestion via REST API
Asynchronous event streaming using Kafka
Raw data storage for replay and debugging
Data processing and cleaning using Spark
Structured storage in PostgreSQL
Analytics APIs with filtering and pagination
Redis caching for improved performance
Dockerized services for easy setup

# Project Phases

# Phase 0 – Basic Setup
Project structure initialization
Virtual environment setup
Git repository initialization
Environment configuration using .env

# Phase 1 – Event Ingestion
FastAPI application setup
/events endpoint implementation
Request validation using Pydantic

# Phase 2 – Kafka Setup
Kafka and Zookeeper setup using Docker

# Phase 3 – Kafka Integration
Event production from FastAPI
Kafka topic creation
End-to-end testing using Postman

# Phase 4 – Consumer Service
Kafka consumer implementation
Event consumption and logging

# Phase 5 – PostgreSQL Setup

# Phase 5A
Database setup
Schema design

# Phase 5B (Architecture Update)
Moved database logic from consumer to processing layer
Introduced separation of concerns
Migrations handled in a dedicated service

# Phase 6 – Analytics APIs
Implemented endpoints:
GET /events
GET /events/count
GET /events/by-type
GET /events/by-user
GET /events/timeline
Added filtering, pagination, and caching

# Phase 7 – Raw Data Storage
Store raw events in JSON files or object storage

# Phase 8 – Data Processing
Read raw events
Clean and transform data
Store structured data in PostgreSQL

# Phase 9 – Updated Analytics APIs
APIs updated to use processed (clean) data

# Project Structure
event-analytics-platform/
│
├── event-ingestion-service/
│   └── app/
│       ├── api/
│       ├── core/
│       ├── schemas/
│       └── producer/
│
├── consumer-service/
│
├── processing-service/
│
├── analytics-service/
│
├── docker-compose.yml
└── README.md

# Getting Started

1. Clone the repository
git clone <your-repo-url>
cd event-analytics-platform

2. Create virtual environment
python -m venv venv
source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt

4. Configure environment variables

# Create a .env file:

KAFKA_BROKER=localhost:9092
POSTGRES_DB=events
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
REDIS_HOST=localhost

5. Start infrastructure services
docker compose up -d

# This will start:

Kafka
Zookeeper
PostgreSQL
Redis

6. Run services

FastAPI (Ingestion Service)
uvicorn app.main:app --reload

Consumer Service
python -m app.consumer

Processing Service (Spark)
python -m app.processing.spark_processor

# Future Improvements
Dead Letter Queue (DLQ) for failed events
Event deduplication using unique event IDs
Workflow scheduling using Apache Airflow
Data lake integration (AWS S3)
Real-time analytics dashboard