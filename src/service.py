from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from hashlib import sha256
from src.db.models import StringToAnalyze
from src.errors.exceptions import (
    StringAlreadyExists,
    InvalidRequestBody,
    InvalidDataType,
)
from .utils import (
    get_string_length,
    is_palindrome,
    count_unique_characters,
    count_words,
    get_character_frequency,
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

        properties = {
            "length": get_string_length(value),
            "is_palindrome": is_palindrome(value),
            "unique_characters": count_unique_characters(value),
            "word_count": count_words(value),
            "sha256_hash": hash_id,
            "character_frequency_map": get_character_frequency(value),
        }

        return {
            "id": record.id,
            "value": record.value,
            "properties": properties,
            "created_at": record.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
