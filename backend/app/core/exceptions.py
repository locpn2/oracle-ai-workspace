from fastapi import HTTPException, status


class OracleVisionException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(OracleVisionException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class AuthorizationError(OracleVisionException):
    def __init__(self, message: str = "Not authorized"):
        super().__init__(message, status_code=403)


class ResourceNotFoundError(OracleVisionException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(f"{resource} not found", status_code=404)


class ValidationError(OracleVisionException):
    def __init__(self, message: str):
        super().__init__(message, status_code=400)


class DatabaseError(OracleVisionException):
    def __init__(self, message: str = "Database error"):
        super().__init__(message, status_code=500)


class DatabaseConnectionError(DatabaseError):
    def __init__(self, message: str = "Database connection failed"):
        super().__init__(message)


class DatabaseQueryError(DatabaseError):
    def __init__(self, message: str = "Database query failed"):
        super().__init__(message)


class LLMError(OracleVisionException):
    def __init__(self, message: str = "LLM processing error"):
        super().__init__(message, status_code=500)


def add_exception_handlers(app):
    @app.exception_handler(OracleVisionException)
    async def oracle_vision_exception_handler(request, exc: OracleVisionException):
        raise HTTPException(status_code=exc.status_code, detail=exc.message)
