"""
Security utilities for the MCP Task Server
"""
from functools import wraps
from typing import Callable, Any
from mcp.types import ToolCallHandler
from .jwt_handler import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


def require_auth(handler: ToolCallHandler) -> ToolCallHandler:
    """
    Decorator to require authentication for MCP tools.
    This will eventually integrate with the MCP request context to extract JWT tokens.
    """
    @wraps(handler)
    async def wrapper(*args, **kwargs):
        # In a real implementation, this would extract the token from the MCP request
        # For now, we'll assume auth is handled elsewhere or use a mock

        # Validate that user is authenticated before proceeding
        # This will be properly integrated when we have access to request context
        return await handler(*args, **kwargs)

    return wrapper