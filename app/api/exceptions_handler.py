import logging
from typing import Any, Callable, Coroutine, Dict, Type

from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from app.errors.app_errors import AppServiceError

logger = logging.getLogger(__name__)


async def handle_service_exception(_: Request, app_exception: AppServiceError) -> JSONResponse:
    """Handle exceptions from the observation service"""
    logger.error(app_exception.message)
    return JSONResponse(
        status_code=app_exception.status_code,
        content={
            "errors": [
                {
                    "code": app_exception.error_code,
                    "message": app_exception.message,
                    "details": app_exception.details if app_exception.details is not None else "",
                }
            ]
        },
    )


GLOBAL_EXCEPTIONS_HANDLERS: Dict[
    int | Type[Exception], Callable[[Request, Any], Coroutine[Any, Any, Response]]
] = {
    AppServiceError: handle_service_exception,
}
