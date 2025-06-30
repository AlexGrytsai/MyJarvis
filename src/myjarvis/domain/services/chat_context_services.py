from __future__ import annotations

from dataclasses import dataclass

from src.myjarvis.domain.exceptions.domain_exceptions import (
    InvalidChatContextServiceError,
)
from src.myjarvis.domain.services.chat_limits_service import (
    ChatContextLimitsService,
)
from src.myjarvis.domain.services.message_expiration_service import (
    MessageExpirationService,
)


@dataclass(frozen=True, slots=True)
class ChatContextServices:
    """Collection of services related to ChatContext.

    This class provides a convenient way to bundle multiple services that
    are related to the ChatContext entity. It is immutable and should be
    used as a single point of access to these services.

    The services currently included are:

    - `ChatContextLimitsService`: responsible for enforcing limits on
      the number of messages and tokens in a chat context.
    - `MessageExpirationService`: responsible for expiring messages in
      a chat context based on their age.
    """

    limits_service: ChatContextLimitsService
    expiration_service: MessageExpirationService

    @classmethod
    def create(
        cls,
        limits_service: ChatContextLimitsService,
        expiration_service: MessageExpirationService,
    ) -> ChatContextServices:
        """Creates an instance of ChatContextServices with custom services.

        This method creates an instance of `ChatContextServices` with the given
        services. The services are immutable and should not be modified after
        being passed to this method.

        Args:
            limits_service: the service responsible for enforcing limits on
                            the chat context.
            expiration_service: the service responsible for expiring messages
                                in the chat context.

        Returns:
            ChatContextServices: an instance with the given services.
        """
        if limits_service is None or expiration_service is None:
            raise InvalidChatContextServiceError(
                "limits_service and expiration_service must not be None"
            )
        return ChatContextServices(
            limits_service=limits_service,
            expiration_service=expiration_service,
        )

    @classmethod
    def create_default(cls) -> ChatContextServices:
        """
        Creates an instance of ChatContextServices with default services.

        The default services are:
        - `ChatContextLimitsService` with `MaxMessagesLimitStrategy` and
          `MaxTokensLimitStrategy`.
        - `MessageExpirationService` with default parameters.

        Returns:
            ChatContextServices: an instance with default services.
        """
        from src.myjarvis.domain.services.chat_limits_service import (
            MaxMessagesLimitStrategy,
            MaxTokensLimitStrategy,
        )

        return cls(
            limits_service=ChatContextLimitsService(
                [
                    MaxMessagesLimitStrategy(),
                    MaxTokensLimitStrategy(),
                ]
            ),
            expiration_service=MessageExpirationService(),
        )
