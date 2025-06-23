from abc import ABC, abstractmethod
from typing import Optional

from src.myjarvis.domain.entities.user import User
from src.myjarvis.domain.value_objects import UserId, Email


class UserRepository(ABC):
    """
    This interface provides a contract for persistence operations related
    to users.
    """

    @abstractmethod
    async def add(self, user: User) -> User:
        """Adds a new user to the repository."""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UserId) -> Optional[User]:
        """Retrieves a user by their unique ID."""
        pass

    @abstractmethod
    async def get_by_email(self, email: Email) -> Optional[User]:
        """Retrieves a user by their email address."""
        pass

    @abstractmethod
    async def get_by_username(self, username: str) -> Optional[User]:
        """Retrieves a user by their username."""
        pass

    @abstractmethod
    async def update(self, user: User) -> None:
        """Updates an existing user in the repository."""
        pass

    @abstractmethod
    async def delete(self, user_id: UserId) -> None:
        """Deletes a user from the repository."""
        pass
