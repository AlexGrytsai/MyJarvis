"""
This module defines the User entity.

The User entity represents a user of the system. Each user can create and manage
multiple AI agents. The user is the root aggregate for the agents they own.

Implementation details:
- The class should be a Pydantic BaseModel for validation.
- It should contain fields like `user_id`, `email`, `created_at`, and an
  optional `telegram_id` for integrations.
- It should have methods for validation, e.g., ensuring the email format is
  correct.
- Business logic related to the user, such as creating an agent, could be
  initiated from this entity or a dedicated domain service.
"""
