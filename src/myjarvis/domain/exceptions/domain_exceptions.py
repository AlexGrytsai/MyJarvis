"""
This module contains all custom exceptions for the domain layer.

These exceptions are raised when a business rule is violated or an expected
condition is not met within the domain logic.

Implementation details:
- A base exception class, e.g., `DomainException`, should be created.
- Specific exceptions should inherit from this base class.
- Examples of specific exceptions include:
  - `UserNotFoundException`
  - `AgentNotFoundException`
  - `NodeNotFoundException`
  - `InvalidActionException`
"""


class DomainException(Exception):
    """Base class for domain-specific exceptions."""
