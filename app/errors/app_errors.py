from typing import Any, NamedTuple


class ErrorsCodes(NamedTuple):
    """List of error codes"""

    internal: str = "APP_SERVICE_NOT_FOUND_ERROR"
    not_found: str = "APP_SERVICE_NOT_FOUND_ERROR"
    neo4j_error: str = "APP_SERVICE_NEO4J_ERROR"


errors_codes = ErrorsCodes()


class AppServiceError(Exception):
    """General exception of the app"""

    def __init__(
        self,
        message: str = "Internal server error",
        error_code: str = errors_codes.internal,
        status_code: int = 500,
        details: Any | None = None,
    ) -> None:
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details
        super().__init__(self.message)


class NotFoundError(AppServiceError):
    """Error for an object not found"""

    def __init__(
        self, message: str, error_code: str = errors_codes.not_found, details: str | None = None
    ) -> None:
        self.message = f"Not Found: {message}"
        self.status_code = 404
        self.error_code = error_code
        self.details = details
        super().__init__(
            message=self.message,
            error_code=self.error_code,
            status_code=self.status_code,
            details=details,
        )


class Neo4JError(AppServiceError):
    """Error with neo4j"""

    def __init__(
        self, message: str, error_code: str = errors_codes.neo4j_error, details: str | None = None
    ) -> None:
        self.message = f"Error with Neo4J: {message}"
        self.status_code = 500
        self.error_code = error_code
        self.details = details
        super().__init__(
            message=self.message,
            error_code=self.error_code,
            status_code=self.status_code,
            details=details,
        )
