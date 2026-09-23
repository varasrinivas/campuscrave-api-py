"""Failures we planned for, and the one place that turns every failure into a response."""

import logging
from datetime import UTC, datetime
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

log = logging.getLogger(__name__)


class ApiError(Exception):
    """A failure we planned for, with the status the browser should see."""

    def __init__(self, status: HTTPStatus, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message


class CanteenClosedError(ApiError):
    def __init__(self, message: str) -> None:
        super().__init__(HTTPStatus.CONFLICT, message)


class NotFoundError(ApiError):
    def __init__(self, message: str) -> None:
        super().__init__(HTTPStatus.NOT_FOUND, message)


class OutOfStockError(ApiError):
    def __init__(self, dish_name: str) -> None:
        super().__init__(HTTPStatus.CONFLICT, f"{dish_name} just sold out")


class TooManyActiveOrdersError(ApiError):
    def __init__(self, maximum: int) -> None:
        super().__init__(
            HTTPStatus.CONFLICT, f"You already have {maximum} orders in flight. Collect one first."
        )


def _body(status: HTTPStatus, message: str) -> dict:
    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "status": status.value,
        "error": status.phrase,
        "message": message or "",
    }


def install_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApiError)
    async def handle_api(_request: Request, ex: ApiError) -> JSONResponse:
        log.warning("%d %s — %s", ex.status.value, ex.status.name, ex.message)
        return JSONResponse(status_code=ex.status.value, content=_body(ex.status, ex.message))

    @app.middleware("http")
    async def handle_everything_else(request: Request, call_next):
        try:
            return await call_next(request)
        except Exception as ex:
            log.exception("Unhandled failure serving request")
            status = HTTPStatus.INTERNAL_SERVER_ERROR
            return JSONResponse(
                status_code=status.value, content=_body(status, f"{type(ex).__name__}: {ex}")
            )
