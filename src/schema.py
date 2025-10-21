from pydantic import BaseModel
from datetime import datetime


class StringRequest(BaseModel):
    value: str


class StringResponse(BaseModel):
    id: str
    value: str
    created_at: datetime
