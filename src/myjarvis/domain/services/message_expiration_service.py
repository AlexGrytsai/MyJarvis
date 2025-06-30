from datetime import datetime
from typing import Callable, Protocol

from src.myjarvis.domain.value_objects import MessageCollection, Message


class ExpirationStrategy(Protocol):
    """
    Protocol for message expiration strategy.
    """

    def is_expired(
        self, message: Message, now: datetime, timeout: int
    ) -> bool:
        pass


class DefaultExpirationStrategy:
    """
    Default strategy for checking if a message is expired.
    """

    @staticmethod
    def is_expired(message: Message, now: datetime, timeout: int) -> bool:
        return (now - message.timestamp).total_seconds() > timeout


class MessageExpirationService:
    """
    Service for removing expired messages from a collection.
    Implements time provider and expiration strategy for flexibility and
    testability.
    """

    def __init__(
        self,
        now_provider: Callable[[], datetime] = datetime.now,
        expiration_strategy: ExpirationStrategy = DefaultExpirationStrategy(),
    ):
        """
        :param now_provider: Function to get the current datetime
                             (for testability)
        :param expiration_strategy: Strategy for checking message expiration
        """
        self._now_provider = now_provider
        self._expiration_strategy = expiration_strategy

    def remove_expired_messages(
        self, messages_collection: MessageCollection, timeout: int
    ) -> MessageCollection:
        """
        Removes expired messages from the collection and returns a new
        collection.
        :param messages_collection: Collection of messages
        :param timeout: Timeout in seconds
        :return: New MessageCollection without expired messages
        """
        if not timeout or timeout <= 0:
            return messages_collection

        now = self._now_provider()
        ids_to_remove = [
            message_id
            for message_id, message in messages_collection.messages.items()
            if self._expiration_strategy.is_expired(message, now, timeout)
        ]

        return messages_collection.partial_remove(ids_to_remove)
