from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List
from uuid import UUID


class EventResponse(BaseModel):
    id: UUID
    event_type: str
    user_id: Optional[str]
    event_timestamp: datetime
    payload: Optional[Dict]
    created_at: datetime

    class Config:
        from_attributes = True

class EventsListResponse(BaseModel):
    total_events: int
    events: List[EventResponse]