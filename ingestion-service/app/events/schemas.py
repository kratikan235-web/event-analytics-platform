from pydantic import BaseModel
from typing import Dict, Any
from datetime import datetime


class EventCreate(BaseModel):
    event_type: str
    user_id: str
    payload: Dict[str, Any]
    timestamp: datetime