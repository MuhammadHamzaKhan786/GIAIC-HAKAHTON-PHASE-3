"""
Standardized error responses for MCP tools
"""
from typing import Union
from pydantic import BaseModel
from enum import Enum


class ErrorCode(str, Enum):
    NOT_FOUND = "NOT_FOUND"
    BAD_REQUEST = "BAD_REQUEST"
    FORBIDDEN = "FORBIDDEN"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"


class MCPErrors(BaseModel):
    code: ErrorCode
    message: str
    details: dict = {}


# Error exceptions
class MCPError(Exception):
    def __init__(self, code: ErrorCode, message: str, details: dict = None):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(message)


class TaskNotFoundError(MCPError):
    def __init__(self, task_id: int):
        super().__init__(
            code=ErrorCode.NOT_FOUND,
            message=f"Task with id {task_id} not found",
            details={"task_id": task_id}
        )


class ValidationError(MCPError):
    def __init__(self, message: str, field: str = None):
        details = {"field": field} if field else {}
        super().__init__(
            code=ErrorCode.BAD_REQUEST,
            message=message,
            details=details
        )


class UnauthorizedError(MCPError):
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(
            code=ErrorCode.FORBIDDEN,
            message=message,
            details={}
        )


class InternalError(MCPError):
    def __init__(self, message: str = "Internal server error"):
        super().__init__(
            code=ErrorCode.INTERNAL_ERROR,
            message=message,
            details={}
        )


# Error handler wrapper
def handle_tool_errors(func):
    """
    Wrapper to handle errors and return standardized MCP error responses
    """
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except TaskNotFoundError as e:
            return MCPErrors(code=e.code, message=e.message, details=e.details)
        except ValidationError as e:
            return MCPErrors(code=e.code, message=e.message, details=e.details)
        except UnauthorizedError as e:
            return MCPErrors(code=e.code, message=e.message, details=e.details)
        except InternalError as e:
            return MCPErrors(code=e.code, message=e.message, details=e.details)
        except Exception as e:
            # Catch-all for unexpected errors
            internal_error = InternalError(str(e))
            return MCPErrors(
                code=internal_error.code,
                message=internal_error.message,
                details=internal_error.details
            )

    return wrapper