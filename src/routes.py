from fastapi import APIRouter, Depends, Query, status, Response
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schema import StringRequest, StringFilterParams
from .service import StringToAnalyzeService
from src.errors.exceptions import InvalidQueryParams

router = APIRouter()
string_analyze_service = StringToAnalyzeService()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_string(
    payload: StringRequest, session: AsyncSession = Depends(get_session)
):
    record = await string_analyze_service.create_string(payload.value, session)
    return record


@router.get("/filter-by-natural-language", status_code=status.HTTP_200_OK)
async def filter_by_natural_language(
    query: str = Query(..., description="Natural language filter query"),
    session: AsyncSession = Depends(get_session),
):
    """
    Interpret a human query like:
    - 'all single word palindromic strings'
    - 'strings longer than 10 characters'
    - 'strings containing the letter z'
    """
    return await string_analyze_service.get_by_natural_language_query(query, session)


@router.get("/{string_value}", status_code=status.HTTP_200_OK)
async def get_string(string_value: str, session: AsyncSession = Depends(get_session)):
    return await string_analyze_service.get_string(string_value, session)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_strings(
    is_palindrome: bool | None = Query(None),
    min_length: int | None = Query(None, ge=0),
    max_length: int | None = Query(None, ge=0),
    word_count: int | None = Query(None, ge=1),
    contains_character: str | None = Query(None, min_length=1, max_length=1),
    session: AsyncSession = Depends(get_session),
):
    """Fetch all analyzed strings with optional filters."""
    try:
        filters = StringFilterParams(
            is_palindrome=is_palindrome,
            min_length=min_length,
            max_length=max_length,
            word_count=word_count,
            contains_character=contains_character,
        )
    except ValueError:
        raise InvalidQueryParams()

    return await string_analyze_service.get_strings(filters, session)


@router.delete(
    "/strings/{string_value}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a string by its value",
    response_description="No content",
)
async def delete_string(
    string_value: str, session: AsyncSession = Depends(get_session)
):
    await StringToAnalyzeService.delete_string(session, string_value)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
