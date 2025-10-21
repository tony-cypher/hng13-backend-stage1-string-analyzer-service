from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from hashlib import sha256
from src.db.models import StringToAnalyze
from src.errors.exceptions import (
    StringAlreadyExists,
    InvalidRequestBody,
    InvalidDataType,
)


class StringToAnalyzeService:
    def generate_sha256(self, value: str) -> str:
        return sha256(value.encode("utf-8")).hexdigest()

    async def create_string(self, value: str, session: AsyncSession):
        if value is None or value == "":
            raise InvalidRequestBody()

        if not isinstance(value, str):
            raise InvalidDataType()

        existing = await session.exec(
            select(StringToAnalyze).where(StringToAnalyze.value == value)
        )
        if existing.first():
            raise StringAlreadyExists()

        hash_id = self.generate_sha256(value)
        record = StringToAnalyze(id=hash_id, value=value)
        session.add(record)
        await session.commit()
        await session.refresh(record)
        return record
