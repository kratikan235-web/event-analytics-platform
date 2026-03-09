from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProcessedEvent(BaseModel):
    event_type: str
    user_id: str
    payload: Optional[dict] = None
    timestamp: str
    processed_at: datetime