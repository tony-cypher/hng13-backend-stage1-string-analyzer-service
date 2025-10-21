from fastapi import HTTPException, status


class StringAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="String already exists in the system",
        )


class InvalidRequestBody(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid request body or missing "value" field',
        )


class InvalidDataType(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail='Invalid data type for "value" (must be string)',
        )
