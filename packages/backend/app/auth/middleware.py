from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_utils import verify_token
from typing import Dict, Optional

security = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict:
    """
    Dependency to get the current user from the JWT token
    """
    token = credentials.credentials

    payload = verify_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str = payload.get("sub")
    email: str = payload.get("email")

    if user_id is None:
        raise HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_data = {"id": user_id, "email": email}
    return user_data


def get_optional_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Optional[Dict]:
    """
    Dependency to get the current user from the JWT token, returning None if invalid
    """
    token = credentials.credentials

    payload = verify_token(token)

    if payload is None:
        return None

    user_id: str = payload.get("sub")
    email: str = payload.get("email")

    if user_id is None:
        return None

    user_data = {"id": user_id, "email": email}
    return user_data