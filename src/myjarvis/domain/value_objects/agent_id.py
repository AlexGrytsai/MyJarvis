"""
This module defines the AgentId value object.

AgentId is a unique identifier for an AIAgent entity. Using a dedicated type
for the ID improves type safety and makes the domain model more explicit.

Implementation details:
- The class should be a Pydantic BaseModel or a simple wrapper around a
  standard type like UUID or int.
- It should be immutable (e.g., using `frozen=True` in Pydantic).
- It can include factory methods for creating new IDs, e.g., `generate()`.
"""
