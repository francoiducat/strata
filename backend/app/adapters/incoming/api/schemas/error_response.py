"""Standard error response schema for all HTTP error responses."""
from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """
    Standard error response returned for all 4xx and 5xx errors.

    422 Unprocessable Entity (validation errors) keep FastAPI's native format.
    """
    code: str    # Machine-readable error code, e.g. "ASSET_NOT_FOUND"
    message: str # Human-readable description
    status: int  # HTTP status code (mirrors the response status)
