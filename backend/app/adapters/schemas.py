from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """DTO for user creation."""

    email: EmailStr
    password: str = Field(min_length=1, description="Password must not be empty")
    full_name: str


class UserPublic(BaseModel):
    """DTO for public user data."""

    id: str
    email: str
    full_name: str
    created_at: datetime


class UserInDB(UserPublic):
    """DTO for internal user retrieval (includes hashed password)."""

    hashed_password: str
    is_active: bool
    updated_at: datetime


class Token(BaseModel):
    """DTO for JWT access and refresh tokens."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    """DTO for login request."""

    email: EmailStr
    password: str


class TokenRefreshRequest(BaseModel):
    """DTO for token refresh request."""

    refresh_token: str
