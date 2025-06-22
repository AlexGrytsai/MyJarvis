"""SQLAlchemy User model.

This module defines the `UserModel` class, which is the SQLAlchemy ORM model
representing the `users` table in the database. It maps the `User` domain entity
to the database schema.

Implementation Details:
- The class should inherit from a declarative base.
- It should define columns corresponding to the `User` entity's attributes:
  - `id`: The primary key, likely a UUID or an integer.
  - `user_id`: A unique identifier for the user (Value Object from domain).
  - `email`: The user's email address, should be unique.
  - `created_at`: Timestamp of when the user was created.
  - `telegram_id`: Optional field for the user's Telegram ID.
- It should define the relationship to the `AgentModel`, indicating that a user
  can have multiple agents (a one-to-many relationship).
  - `agents = relationship("AgentModel", back_populates="user")`
""" 