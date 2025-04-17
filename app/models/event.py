from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel

class GridEvent(BaseModel):
    id: str
    subject: str
    event_type: str
    data: Dict[str, Any]
    event_time: datetime
    data_version: Optional[str] = None
    topic: Optional[str] = None
    metadata_version: Optional[str] = None

class CloudEvent(BaseModel):
    id: str
    source: str
    type: str
    data: Dict[str, Any]
    time: datetime
    specversion: str
    datacontenttype: Optional[str] = None
    subject: Optional[str] = None