from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi import FastAPI
from .exceptions import (
    InvalidQueryParams,
    UnableToParseQuery,
    ConflictingFilters,
    StringAlreadyExists,
    InvalidRequestBody,
    InvalidDataType,
    StringNotFound,
)


def register_exception_handlers(app: FastAPI):
    """Registers all custom exception handlers for the app."""

    @app.exception_handler(StringAlreadyExists)
    async def strings_already_exists_handler(
        request: Request, exc: StringAlreadyExists
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(InvalidRequestBody)
    async def invalid_request_body_handler(request: Request, exc: InvalidRequestBody):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(InvalidDataType)
    async def invalid_data_type_handler(request: Request, exc: InvalidDataType):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(StringNotFound)
    async def string_not_found_handler(request: Request, exc: StringNotFound):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(InvalidQueryParams)
    async def invalid_query_params_handler(request: Request, exc: InvalidQueryParams):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(UnableToParseQuery)
    async def unable_to_parse_query_handler(request: Request, exc: UnableToParseQuery):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    @app.exception_handler(ConflictingFilters)
    async def conflicting_filters_handler(request: Request, exc: ConflictingFilters):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
