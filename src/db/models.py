from sqlmodel import SQLModel, Field
from hashlib import sha256
from datetime import datetime


def generate_sha256(value: str) -> str:
    return sha256(value.encode("utf-8")).hexdigest()


class StringToAnalyze(SQLModel, table=True):
    __tablename__ = "string_to_analyze"

    id: str = Field(default=None, primary_key=True, index=True)
    value: str
    created_at: datetime = Field(default_factory=lambda: datetime.utcnow())
