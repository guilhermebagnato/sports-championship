from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.adapters.repositories import UserRepository
from app.application.ports import IAuthService, IUserRepository
from app.application.services import AuthService
from app.auth import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY, oauth2_scheme
from app.database import get_session
from app.domain.entities import User as UserEntity

# Session dependency
SessionDep = Annotated[Session, Depends(get_session)]


# User repository dependency
def get_user_repository(session: SessionDep) -> IUserRepository:
    """Get user repository."""
    return UserRepository(session)


RepositoryDep = Annotated[IUserRepository, Depends(get_user_repository)]


# Auth service dependency
def get_auth_service() -> IAuthService:
    """Get auth service."""
    return AuthService(
        secret_key=SECRET_KEY,
        algorithm=ALGORITHM,
        expire_minutes=ACCESS_TOKEN_EXPIRE_MINUTES,
    )


AuthServiceDep = Annotated[IAuthService, Depends(get_auth_service)]


# Current user dependency
async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    auth_service: AuthServiceDep,
    repository: RepositoryDep,
) -> UserEntity | None:
    """Get current authenticated user from JWT token.

    Args:
        token: JWT token from Authorization header
        auth_service: Auth service for token decoding
        repository: User repository for retrieving user

    Returns:
        User entity if token is valid and user exists, None otherwise
    """
    user_id = auth_service.decode_token(token)
    if user_id is None:
        return None

    return await repository.get_by_id(user_id)


CurrentUserDep = Annotated[UserEntity | None, Depends(get_current_user)]
