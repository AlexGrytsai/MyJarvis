"""SQLAlchemy implementation of the UserRepository.

This module provides a concrete implementation of the `UserRepository` interface
defined in the domain layer. It uses SQLAlchemy for data persistence.

Implementation Details:
- The class `SQLAlchemyUserRepository` should inherit from `UserRepository`.
- It will require an `AsyncSession` to be injected for database communication.
- It must implement all the methods from the interface, such as:
  - `add(user: User)`: Adds a new user to the database. This involves creating a
    `UserModel` instance from the `User` entity and adding it to the session.
  - `get_by_id(user_id: UserID)`: Retrieves a user by their unique ID. This involves
    querying the `UserModel` table and converting the result back to a `User` entity.
  - `get_by_email(email: str)`: Retrieves a user by their email address.
  - `list()`: Retrieves all users.
- A private method `_to_entity` could be used to map from `UserModel` to `User` entity,
  and `_from_entity` to map from the entity to the model. This separates the mapping
  logic from the data access logic.
""" 