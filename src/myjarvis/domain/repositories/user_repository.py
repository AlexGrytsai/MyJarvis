"""
This module defines the repository interface for the User entity.

This interface provides a contract for persistence operations related to users,
abstracting the underlying data storage mechanism.

Implementation details:
- The interface should be an abstract base class (ABC).
- It should define asynchronous methods for CRUD operations, such as:
  - `add(user: User) -> None`
  - `get_by_id(user_id: UserId) -> User | None`
  - `get_by_email(email: str) -> User | None`
  - `update(user: User) -> None`
  - `delete(user_id: UserId) -> None`
- Implementations of this interface will reside in the infrastructure layer.
"""
