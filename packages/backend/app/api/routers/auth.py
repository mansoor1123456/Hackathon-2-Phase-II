from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlmodel import Session
from datetime import timedelta
from ...database.session import get_session
from ...models.user import UserCreate, UserPublic
from ...schemas.user import UserLogin, Token
from ...services.user_service import UserService
from ...auth.jwt_utils import create_access_token, verify_password
from uuid import UUID

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()


@router.post("/register", response_model=UserPublic)
def register(user_data: UserCreate, session: Session = Depends(get_session)):
    """
    Register a new user.
    """
    try:
        user = UserService.create_user(session, user_data)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
def login(user_credentials: UserLogin, session: Session = Depends(get_session)):
    """
    Authenticate user and return access token.
    """
    user = UserService.authenticate_user(
        session,
        user_credentials.email,
        user_credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)  # This should come from env
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/logout")
def logout():
    """
    Logout user (client-side token invalidation).
    """
    # In a stateless JWT system, logout is typically handled client-side
    # by removing the token from client storage
    return {"message": "Logged out successfully"}