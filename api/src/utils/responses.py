import logging
import traceback
from pathlib import Path
from typing import Any

from fastapi.responses import FileResponse, JSONResponse

_log = logging.getLogger(__name__)


class JSONErrorResponse(JSONResponse):
    """Base class for JSON error responses."""

    def __init__(
        self, status_code: int, message: str, ctx: dict[str, Any] | None = None
    ):
        super().__init__(
            content=dict(
                error_message=message,
                error_details={} if ctx is None else ctx,
            ),
            status_code=status_code,
        )


class JSONNotFound(JSONErrorResponse):
    """404 Not Found."""

    def __init__(self, message: str, ctx: dict[str, Any] | None = None):
        super().__init__(404, f"Not Found: {message}", ctx)


class JSONBadRequest(JSONErrorResponse):
    """400 Bad Request."""

    def __init__(self, message: str, ctx: dict[str, Any] | None = None):
        super().__init__(400, f"Bad Request: {message}", ctx)


class JSONConflict(JSONErrorResponse):
    """409 Conflict."""

    def __init__(self, message: str, ctx: dict[str, Any] | None = None):
        super().__init__(409, f"Conflict: {message}", ctx)


class JSONInternalServerError(JSONResponse):
    """500 Internal Server Error."""

    def __init__(self, err: Exception, ctx: dict[str, Any] | None = None):
        """
        Args:
            err (Exception): The exception that caused the error.
            ctx (dict[str, Any] | None): Additional context.
        """
        super().__init__(
            content=dict(
                error_message=f"Internal Server Error: {err}",
                error_type=type(err).__name__,
                error_details={} if ctx is None else ctx,
                error_traceback=traceback.format_exception(err) or [],
            ),
            status_code=500,
        )


class SelfDestructFileResponse(FileResponse):
    """FileResponse that deletes the file after it has been sent."""

    def __del__(self):
        _log.debug(f"Deleting file {self.path}")
        Path(self.path).unlink(missing_ok=True)
