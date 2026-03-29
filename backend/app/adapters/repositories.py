from sqlmodel import Session, select

from app.adapters.models import User as UserModel
from app.application.ports import IUserRepository
from app.domain.entities import User as UserEntity


class UserRepository(IUserRepository):
    """User Repository - Database Adapter.

    Implements IUserRepository port using SQLModel/SQLAlchemy.
    Bridges domain entities with database models.
    """

    def __init__(self, session: Session) -> None:
        """Initialize UserRepository.

        Args:
            session: SQLModel database session
        """
        self.session = session

    async def get_by_email(self, email: str) -> UserEntity | None:
        """Retrieve user by email address.

        Args:
            email: User email to search for

        Returns:
            User domain entity or None if not found
        """
        statement = select(UserModel).where(UserModel.email == email)
        db_user = self.session.exec(statement).first()

        if db_user is None:
            return None

        return self._model_to_entity(db_user)

    async def get_by_id(self, user_id: str) -> UserEntity | None:
        """Retrieve user by ID.

        Args:
            user_id: User ID to search for

        Returns:
            User domain entity or None if not found
        """
        db_user = self.session.get(UserModel, user_id)

        if db_user is None:
            return None

        return self._model_to_entity(db_user)

    async def create(self, user: UserEntity) -> UserEntity:
        """Create new user in database.

        Args:
            user: User domain entity to create

        Returns:
            Created user domain entity with ID
        """
        db_user = UserModel(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            hashed_password=user.hashed_password,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return self._model_to_entity(db_user)

    async def update(self, user: UserEntity) -> UserEntity:
        """Update existing user.

        Args:
            user: User domain entity with updated values

        Returns:
            Updated user domain entity
        """
        db_user = self.session.get(UserModel, user.id)

        if db_user is None:
            raise ValueError(f"User with id {user.id} not found")

        db_user.email = user.email
        db_user.full_name = user.full_name
        db_user.hashed_password = user.hashed_password
        db_user.is_active = user.is_active
        db_user.updated_at = user.updated_at

        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        return self._model_to_entity(db_user)

    @staticmethod
    def _model_to_entity(db_user: UserModel) -> UserEntity:
        """Convert database model to domain entity.

        Args:
            db_user: SQLModel User instance

        Returns:
            Domain User entity
        """
        from typing import cast

        return UserEntity(
            id=cast(str, db_user.id),  # id is never None after DB retrieval
            email=db_user.email,
            full_name=db_user.full_name,
            hashed_password=db_user.hashed_password,
            is_active=db_user.is_active,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        )
