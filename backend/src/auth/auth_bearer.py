from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, status, Depends
from backend.src.auth.jwt_handler import verify_token
from typing import Dict, Optional

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid authentication scheme."
                )
            token = self.verify_jwt(credentials.credentials)
            if not token:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code."
            )

    def verify_jwt(self, jwtoken: str) -> Optional[Dict]:
        try:
            print(f"DEBUG: Verifying token: {jwtoken[:20]}..." if jwtoken else 'None')  # Log first 20 chars to avoid printing full token
            payload = verify_token(jwtoken)
            print(f"DEBUG: Token payload: {payload}")
            return payload
        except Exception as e:
            print(f"DEBUG: Token verification failed: {str(e)}")
            return None

# Dependency for protected routes
async def get_current_user_from_token(token: str = Depends(JWTBearer())) -> Dict:
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload