from fastapi import APIRouter, Depends, status
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .schema import StringRequest, StringResponse
from .service import StringToAnalyzeService

string_router = APIRouter()
string_analyze_service = StringToAnalyzeService()


@string_router.post(
    "/strings", response_model=StringResponse, status_code=status.HTTP_201_CREATED
)
async def create_string(
    payload: StringRequest, session: AsyncSession = Depends(get_session)
):
    record = await string_analyze_service.create_string(payload.value, session)
    formatted_date = record.created_at.strftime("%Y-%m-%dT%H:%M:%SZ")
    return {"id": record.id, "value": record.value, "created_at": formatted_date}
