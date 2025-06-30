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


class WrongIdType(DomainException):
    """Raised when the id type is not valid."""


class WrongDatatimeType(DomainException):
    """Raised when the datetime type is not valid."""


class EmailNotValid(DomainException):
    """Raised when the email is not valid."""


class NewEmailSameAsCurrent(DomainException):
    """Raised when the new email is the same as the current email."""


class NewUsernameSameAsCurrent(NewEmailSameAsCurrent):
    """Raised when the new username is the same as the current username."""


class LLMProviderAlreadyExistsInUser(DomainException):
    """Raised when the LLM provider already exists."""


class LLMProviderNotExistsInUser(DomainException):
    """Raised when the LLM provider does not exist in the user."""


class TemperatureNotValid(DomainException):
    """Raised when the temperature is not valid."""


class MaxTokensNotValid(DomainException):
    """Raised when the max tokens is not valid."""


class AgentNotFoundInUser(DomainException):
    """Raised when the agent is not found in the user."""


class UnavailableAgentName(DomainException):
    """
    Raised when the user tries to create or update an agent with an
    unavailable name.
    """


class MessageException(DomainException):
    """Raised when a message is not found."""


class MessageWithoutId(MessageException):
    """Raised when a message ID is not found."""


class MessageCouldNotBeEmpty(MessageException):
    """Raised when a message is not found."""


class MessageTooLong(MessageException):
    """Raised when a message is too long."""


class MessageHasInvalidParentId(MessageException):
    """Raised when a message has an invalid parent ID."""


class AttachmentsToMessageInWrongFormat(MessageException):
    """Raised when attachments are not in the correct format."""


class MessageMetaDataWrongFormat(MessageException):
    """Raised when a metadata's message transmitted in the wrong format."""


class MaxMessagesNotValid(DomainException):
    """Raised when the max messages is not valid."""


class InvalidMessageRole(DomainException):
    """Raised when a message role is not valid."""


class AgentIdRequired(DomainException):
    """Raised when an agent ID is required, but not provided."""


class UserIdRequired(DomainException):
    """Raised when a user ID is required, but not provided."""


class ContextIdInvalidFormat(DomainException):
    """Raised when a context ID is not in the correct format."""


class TimeoutNotValid(DomainException):
    """Raised when the timeout is not valid."""


class MessagesListNotValid(DomainException):
    """Raised when the messages list is not valid."""


class MessageNotFound(DomainException):
    """Raised when a message is not found."""


class UnexpectedException(DomainException):
    """Raised when an unexpected exception is raised."""


class InvalidChatContextServiceError(DomainException):
    pass
