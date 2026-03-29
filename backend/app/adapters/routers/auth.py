"""Authentication router."""

from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from app.adapters.schemas import UserCreate, UserPublic
from app.dependencies import AuthServiceDep, RepositoryDep
from app.domain.entities import User as UserEntity

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/register", response_model=UserPublic, status_code=status.HTTP_201_CREATED
)
async def register(
    user_create: UserCreate,
    auth_service: AuthServiceDep,
    repository: RepositoryDep,
) -> UserPublic:
    """Register a new user.

    Args:
        user_create: User registration data (email, password, full_name)
        auth_service: Service for password hashing and JWT operations
        repository: Repository for user persistence

    Returns:
        UserPublic with created user data (without password)

    Raises:
        HTTPException 400: If email already registered
    """
    # Check if email already registered
    existing_user = await repository.get_by_email(user_create.email)
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    # Hash password
    hashed_password = auth_service.hash_password(user_create.password)

    # Create user entity
    user_entity = UserEntity(
        id=str(uuid4()),
        email=user_create.email,
        full_name=user_create.full_name,
        hashed_password=hashed_password,
        is_active=True,
    )

    # Persist user
    created_user = await repository.create(user_entity)

    # Return public representation (without password)
    return UserPublic(
        id=created_user.id,
        email=created_user.email,
        full_name=created_user.full_name,
        created_at=created_user.created_at,
    )


# TODO: Implement in Phase 2
# POST /token (login)
# POST /refresh (refresh token)
