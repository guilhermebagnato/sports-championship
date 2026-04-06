"""Authentication router."""

from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from app.adapters.schemas import LoginRequest, Token, UserCreate, UserPublic
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


@router.post("/token", response_model=Token)
async def login(
    login_data: LoginRequest,
    auth_service: AuthServiceDep,
    repository: RepositoryDep,
) -> Token:
    """Login to get access token.

    Args:
        login_data: Login credentials (email, password)
        auth_service: Service for password verification and JWT operations
        repository: Repository for user retrieval

    Returns:
        Token with access_token and token_type

    Raises:
        HTTPException 401: If invalid credentials
    """
    user = await repository.get_by_email(login_data.email)
    if user is None or not auth_service.verify_password(
        login_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account is disabled",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = auth_service.create_access_token(user_id=user.id)
    return Token(access_token=access_token)


# TODO: Implement in Phase 2
# POST /refresh (refresh token)
