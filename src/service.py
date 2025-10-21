from sqlmodel.ext.asyncio.session import AsyncSession
from hashlib import sha256
from datetime import datetime, timezone
from src.db.models import StringToAnalyze


class StringToAnalyzeService:
    def generate_sha256(self, value: str) -> str:
        return sha256(value.encode("utf-8")).hexdigest()

    def format_datetime_z(self, dt: datetime) -> str:
        return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    async def create_string(self, value: str, session: AsyncSession):
        hash_id = self.generate_sha256(value)

        record = StringToAnalyze(id=hash_id, value=value)
        session.add(record)
        await session.commit()
        await session.refresh(record)
        return record
