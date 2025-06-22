"""
This module defines the UserId value object.

UserId is a unique identifier for a User entity. Using a dedicated type for the
ID improves type safety and makes the domain model more explicit.

Implementation details:
- The class should be a Pydantic BaseModel or a simple wrapper around a
  standard type like UUID, int, or string, depending on the identity provider
  (e.g., Firebase Auth).
- It should be immutable (e.g., using `frozen=True` in Pydantic).
"""
