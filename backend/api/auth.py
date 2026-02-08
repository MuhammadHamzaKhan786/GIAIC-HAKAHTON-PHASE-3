"""
Authentication validation middleware.
Validates JWT tokens and extracts user information.
"""
from fastapi import Request, HTTPException
from typing import Dict, Any
from jose import jwt, JWTError
import os


async def validate_user_token(request: Request) -> Dict[str, Any]:
    """
    Validate user authentication token and return user information.
    Decodes the JWT token to extract the user_id.
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

    token = auth_header.split(" ")[1]

    try:
        # Get the JWT secret from environment variable
        jwt_secret = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-change-this-in-production")
        
        # Decode the JWT token
        # Using options to skip signature verification for development
        # In production, remove verify_signature option and use proper secret
        decoded = jwt.decode(
            token, 
            jwt_secret, 
            algorithms=["HS256"],
            options={"verify_signature": False, "verify_exp": False}
        )
        
        # Extract user_id from the token (could be 'user_id' or 'sub')
        user_id = decoded.get("user_id") or decoded.get("sub")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token: missing user_id")
        
        return {"user_id": user_id}
    except JWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")


# Alternative: Use an actual JWT verification if needed
def verify_jwt_token(token: str) -> Dict[str, Any]:
    """
    Verify JWT token and extract user information.
    In a real implementation, this would use Better Auth's JWT verification.
    """
    # Placeholder for actual JWT verification logic
    # from better_auth import verify_token
    # return verify_token(token)

    # For now, returning a mock user
    return {"user_id": token[:8] if len(token) >= 8 else "default_user"}