from pydantic import BaseModel, Field, field_validator
from typing import Optional, Dict, Any


class StringRequest(BaseModel):
    value: str


class StringFilterParams(BaseModel):
    is_palindrome: Optional[bool] = Field(
        None, description="Whether string is palindrome"
    )
    min_length: Optional[int] = Field(None, ge=0, description="Minimum string length")
    max_length: Optional[int] = Field(None, ge=0, description="Maximum string length")
    word_count: Optional[int] = Field(None, ge=1, description="Exact word count")
    contains_character: Optional[str] = Field(
        None, description="Single character to search for"
    )

    @field_validator("contains_character")
    @classmethod
    def validate_single_char(cls, v: Optional[str]) -> Optional[str]:
        if v and len(v) != 1:
            raise ValueError("contains_character must be a single character")
        return v


class StringProperties(BaseModel):
    length: int
    is_palindrome: bool
    unique_characters: int
    word_count: int
    sha256_hash: str
    character_frequency_map: Dict[str, int]


class StringResponse(BaseModel):
    id: str
    value: str
    properties: StringProperties
    created_at: str


class StringListResponse(BaseModel):
    data: list[StringResponse]
    count: int
    filters_applied: Dict[str, Any]
