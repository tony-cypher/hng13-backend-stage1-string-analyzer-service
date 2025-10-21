from sqlmodel import SQLModel, Field, Column
from sqlalchemy import DateTime
from datetime import datetime, timezone


class StringToAnalyze(SQLModel, table=True):
    __tablename__ = "string_to_analyze"

    id: str = Field(default=None, primary_key=True, index=True)
    value: str = Field(nullable=False)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True)),
        default_factory=lambda: datetime.now(timezone.utc),
    )
