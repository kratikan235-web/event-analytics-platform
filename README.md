# Event Analytics Platform

An event-driven backend analytics system built using FastAPI, Kafka, PostgreSQL, Redis, and Docker.

The platform receives events from APIs, processes them asynchronously using Kafka consumers, stores processed data in PostgreSQL, and exposes analytics APIs for querying insights.

# Architecture Flow

Client
  ↓
FastAPI (Event Ingestion API)
  ↓
Kafka (Event Queue / Buffer)
  ↓
Consumer Service
  ↓
PostgreSQL (Processed Data)
  ↓
Analytics APIs
  ↓
Redis Cache

# Tech Stack

Python
FastAPI
Kafka
PostgreSQL
Redis
Docker
SQLAlchemy
Pydantic

# Project Phases

This project was developed step-by-step to simulate a real event-processing backend architecture.

# Phase 0 – Basic Setup

Created project structure
Setup Python virtual environment
Initialized Git repository

# Phase 1 – Event Ingestion Service

Created FastAPI application
Implemented /events API
Added request validation using Pydantic

# Phase 2 – Kafka Setup

Setup Kafka locally using Docker
Created Kafka broker and Zookeeper

# Phase 3 – Kafka Integration

Integrated FastAPI with Kafka producer
Published events to Kafka topics
Tested event flow using Postman

# Phase 4 – Consumer Service

Built Kafka consumer service
Consumed events from Kafka
Added logging and error handling

# Phase 5 – PostgreSQL Storage

# Phase 5A

Setup PostgreSQL database
Created events table schema

# Phase 5B

Processed Kafka events
Stored processed events in PostgreSQL

# Phase 6 – Analytics APIs
Built analytics endpoints for querying event data.

# Endpoints implemented:

GET /events
GET /events/count
GET /events/by-type
GET /events/by-user
GET /events/timeline

# Features:

Event filtering
Pagination
Redis caching for faster responses

# Project Structure
event-analytics-platform
│
├── event-ingestion-service
│   ├── app
│   │   ├── api
│   │   ├── core
│   │   ├── db
│   │   └── schemas
│
├── consumer-service
│
├── docker-compose.yml
└── README.md

# How to Run the Project
1 Install dependencies
pip install -r requirements.txt
2 Start services using Docker
docker compose up -d

This starts:
Kafka
Zookeeper
PostgreSQL
Redis

3 Run FastAPI service
uvicorn app.main:app --reload

# Future Improvements

Add Spark for batch analytics
Store raw events in data lake
Add dashboard for analytics visualization