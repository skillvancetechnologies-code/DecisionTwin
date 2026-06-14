"""Domain errors and a consistent error payload shape."""
from fastapi import HTTPException, status


class ValidationFailed(HTTPException):
    """Raised when an uploaded CSV fails validation.

    Produces the documented 400 body:
        {"error": "VALIDATION_FAILED", "details": [...]}
    """

    def __init__(self, details: list[dict]):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "VALIDATION_FAILED", "details": details},
        )


class NotFound(HTTPException):
    def __init__(self, what: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "NOT_FOUND", "message": f"{what} not found"},
        )
