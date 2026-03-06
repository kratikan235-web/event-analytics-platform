from fastapi import APIRouter, Depends
from sqlalchemy import func

from app.db.models import Event
from datetime import datetime
from typing import Optional
from app.schemas.event import EventsListResponse
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.core.redis_client import redis_client
import json

router = APIRouter()

# Filtered Events
@router.get("/events", response_model=EventsListResponse)
def get_events(
    user_id: Optional[str] = None,
    event_type: Optional[str] = None,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
    limit: int = 100,
    offset: int = 0,
    db: Session = Depends(get_db)
):

    # Create unique cache key
    cache_key = f"events:{user_id}:{event_type}:{start}:{end}:{limit}:{offset}"

    print("CACHE KEY:", cache_key)

    # Check cache
    cached_data = redis_client.get(cache_key)

    if cached_data:
        print("CACHE HIT")
        return EventsListResponse(**json.loads(cached_data))
    print("CACHE MISS - DB QUERY")

    # DB query
    query = db.query(Event)

    if user_id:
        query = query.filter(Event.user_id == user_id)

    if event_type:
        query = query.filter(Event.event_type == event_type)

    if start:
        query = query.filter(Event.event_timestamp >= start)

    if end:
        query = query.filter(Event.event_timestamp <= end)

    total_events = query.count()
    events = query.offset(offset).limit(limit).all()

    # Convert to Pydantic response
    response = EventsListResponse(
        total_events=total_events,
        events=events
    )

    # Save in Redis (60 sec cache)
    redis_client.setex(
        cache_key,
        60,
        json.dumps(response.model_dump(), default=str)
    )

    return response

# Events by Count
@router.get("/events/count")
def get_event_count(db: Session = Depends(get_db)):
    count = db.query(func.count(Event.id)).scalar()
    return {
        "total_events": count
    }

# Events by Type
@router.get("/events/by-type")
def events_by_type(db: Session = Depends(get_db)):
    results = (
        db.query(Event.event_type, func.count(Event.id))
        .group_by(Event.event_type)
        .all()
    )

    data = {event_type: count for event_type, count in results}

    return data

# Events by User
@router.get("/events/by-user")
def events_by_user(db: Session = Depends(get_db)):
    results = (
        db.query(Event.user_id, func.count(Event.id))
        .group_by(Event.user_id)
        .all()
    )

    data = {user_id: count for user_id, count in results}

    return data

# Events Timeline
@router.get("/events/timeline")
def events_timeline(db: Session = Depends(get_db)):
    results = (
        db.query(
            func.date(Event.event_timestamp),
            func.count(Event.id)
        )
        .group_by(func.date(Event.event_timestamp))
        .all()
    )

    return {str(date): count for date, count in results}