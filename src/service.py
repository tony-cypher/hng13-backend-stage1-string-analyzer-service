import re
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select
from hashlib import sha256
from typing import Dict
from datetime import datetime, timezone
from src.db.models import StringToAnalyze
from src.errors.exceptions import (
    StringAlreadyExists,
    InvalidRequestBody,
    InvalidDataType,
    StringNotFound,
    InvalidQueryParams,
    ConflictingFilters,
    UnableToParseQuery,
)
from .schema import StringFilterParams
from .utils import (
    get_string_length,
    is_palindrome,
    count_unique_characters,
    count_words,
    get_character_frequency,
)


class StringToAnalyzeService:
    @staticmethod
    def generate_sha256(value: str) -> str:
        return sha256(value.encode("utf-8")).hexdigest()

    @staticmethod
    def utc_now_z() -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    @staticmethod
    def _analyze_string(value: str) -> Dict:
        clean_value = value.strip()
        return {
            "length": len(clean_value),
            "is_palindrome": clean_value.lower() == clean_value[::-1].lower(),
            "unique_characters": len(set(clean_value)),
            "word_count": len(clean_value.split()),
            "sha256_hash": StringToAnalyzeService.generate_sha256(clean_value),
            "character_frequency_map": {
                char: clean_value.count(char) for char in set(clean_value)
            },
        }

    @staticmethod
    def _build_response(record: StringToAnalyze) -> dict:
        value = record.value
        properties = {
            "length": get_string_length(value),
            "is_palindrome": is_palindrome(value),
            "unique_characters": count_unique_characters(value),
            "word_count": count_words(value),
            "sha256_hash": record.id,
            "character_frequency_map": get_character_frequency(value),
        }

        return {
            "id": record.id,
            "value": record.value,
            "properties": properties,
            "created_at": record.created_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
        }

    @staticmethod
    def parse_natural_language_query(query: str) -> Dict:
        if not query or not query.strip():
            raise UnableToParseQuery(query)

        query_lower = query.lower().strip()
        filters = {}

        # --- Palindrome related ---
        if "palindromic" in query_lower or "palindrome" in query_lower:
            filters["is_palindrome"] = True

        # --- Single or multiple word conditions ---
        if "single word" in query_lower or "one word" in query_lower:
            filters["word_count"] = 1
        elif "two word" in query_lower or "double word" in query_lower:
            filters["word_count"] = 2

        # --- Length conditions ---
        match_longer = re.search(r"longer than (\d+)", query_lower)
        if match_longer:
            filters["min_length"] = int(match_longer.group(1)) + 1

        match_shorter = re.search(r"shorter than (\d+)", query_lower)
        if match_shorter:
            filters["max_length"] = int(match_shorter.group(1)) - 1

        match_exact_length = re.search(r"exactly (\d+) characters?", query_lower)
        if match_exact_length:
            filters["min_length"] = filters["max_length"] = int(
                match_exact_length.group(1)
            )

        # --- Character filters ---
        match_contains = re.search(
            r"(contain|containing|includes?) the letter (\w)", query_lower
        )
        if match_contains:
            filters["contains_character"] = match_contains.group(2)

        # --- Vowel heuristic ---
        if "first vowel" in query_lower:
            filters["contains_character"] = "a"

        # Validate conflicts (e.g., impossible length logic)
        if (
            "min_length" in filters
            and "max_length" in filters
            and filters["min_length"] > filters["max_length"]
        ):
            raise ConflictingFilters()

        if not filters:
            raise UnableToParseQuery(query)

        return filters

    async def create_string(self, value: str, session: AsyncSession) -> dict:
        if value is None or value == "":
            raise InvalidRequestBody()

        if not isinstance(value, str):
            raise InvalidDataType()

        existing = await session.exec(
            select(StringToAnalyze).where(StringToAnalyze.value == value)
        )
        if existing.first():
            raise StringAlreadyExists()

        hash_id = StringToAnalyzeService.generate_sha256(value)
        record = StringToAnalyze(id=hash_id, value=value)
        session.add(record)
        await session.commit()
        await session.refresh(record)

        return self._build_response(record)

    async def get_string(self, value: str, session: AsyncSession) -> dict:
        hash_id = StringToAnalyzeService.generate_sha256(value)
        result = await session.exec(
            select(StringToAnalyze).where(StringToAnalyze.id == hash_id)
        )
        record = result.scalar_one_or_none()

        if not record:
            raise StringNotFound()

        return StringToAnalyzeService._build_response(record)

    async def get_strings(
        self, filters: StringFilterParams, session: AsyncSession
    ) -> Dict:
        try:
            query = select(StringToAnalyze)
            results = await session.exec(query)
            records = results.scalars().all()

            data = []
            for record in records:
                props = StringToAnalyzeService._analyze_string(record.value)

                # Apply filters (Python-side filtering for simplicity)
                if (
                    filters.is_palindrome is not None
                    and props["is_palindrome"] != filters.is_palindrome
                ):
                    continue
                if (
                    filters.min_length is not None
                    and props["length"] < filters.min_length
                ):
                    continue
                if (
                    filters.max_length is not None
                    and props["length"] > filters.max_length
                ):
                    continue
                if (
                    filters.word_count is not None
                    and props["word_count"] != filters.word_count
                ):
                    continue
                if (
                    filters.contains_character
                    and filters.contains_character not in record.value
                ):
                    continue

                data.append(StringToAnalyzeService._build_response(record))

            return {
                "data": data,
                "count": len(data),
                "filters_applied": {
                    k: v for k, v in filters.model_dump().items() if v is not None
                },
            }

        except Exception as e:
            raise InvalidQueryParams() from e

    async def get_by_natural_language_query(
        self, query: str, session: AsyncSession
    ) -> Dict:
        parsed_filters = StringToAnalyzeService.parse_natural_language_query(query)
        filters_model = StringFilterParams(**parsed_filters)

        result = await self.get_strings(filters_model, session)

        return {
            "data": result["data"],
            "count": result["count"],
            "interpreted_query": {
                "original": query,
                "parsed_filters": parsed_filters,
            },
        }
