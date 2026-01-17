from sqlmodel import Session, select
from typing import Optional
from ..models.user import User, UserCreate, UserUpdate
from ..auth.jwt_utils import get_password_hash, verify_password
from uuid import UUID


class UserService:
    @staticmethod
    def get_user_by_id(session: Session, user_id: UUID) -> Optional[User]:
        """Get a user by their ID"""
        statement = select(User).where(User.id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def get_user_by_email(session: Session, email: str) -> Optional[User]:
        """Get a user by their email"""
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

    @staticmethod
    def create_user(session: Session, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if user with this email already exists
        existing_user = UserService.get_user_by_email(session, user_data.email)
        if existing_user:
            raise ValueError("A user with this email already exists")

        # Hash the password
        password_hash = get_password_hash(user_data.password)

        # Create the user object
        user = User(
            email=user_data.email,
            name=user_data.name,
            password_hash=password_hash
        )

        # Add to session and commit
        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    @staticmethod
    def update_user(session: Session, user_id: UUID, user_data: UserUpdate) -> Optional[User]:
        """Update a user"""
        user = UserService.get_user_by_id(session, user_id)

        if not user:
            return None

        # Update fields if they are provided
        if user_data.name is not None:
            user.name = user_data.name
        if user_data.email is not None:
            # Check if new email is already taken
            existing_user = UserService.get_user_by_email(session, user_data.email)
            if existing_user and existing_user.id != user_id:
                raise ValueError("A user with this email already exists")
            user.email = user_data.email
        if user_data.is_active is not None:
            user.is_active = user_data.is_active

        session.add(user)
        session.commit()
        session.refresh(user)

        return user

    @staticmethod
    def delete_user(session: Session, user_id: UUID) -> bool:
        """Delete a user"""
        user = UserService.get_user_by_id(session, user_id)

        if not user:
            return False

        session.delete(user)
        session.commit()

        return True

    @staticmethod
    def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user by email and password"""
        user = UserService.get_user_by_email(session, email)

        if not user or not verify_password(password, user.password_hash):
            return None

        return user