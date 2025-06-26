from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Union
from uuid import UUID

from src.myjarvis.domain.exceptions import MessageNotFound
from src.myjarvis.domain.services import MessageExpirationService
from src.myjarvis.domain.value_objects import Message


@dataclass(frozen=True, slots=True)
class MessageCollection:
    messages: Dict[UUID, Message] = field(default_factory=dict)
    message_expiration_service: MessageExpirationService = field(
        default_factory=MessageExpirationService
    )

    @property
    def total_tokens(self) -> int:
        """Returns the total number of tokens in the collection."""
        return sum(message.total_tokens for message in self.messages.values())

    @property
    def total_messages(self) -> int:
        """Returns the total number of messages in the collection."""
        return len(self.messages)

    @classmethod
    def create(
        cls,
        messages: Optional[Union[List[Message], Dict[UUID, Message]]] = None,
    ) -> MessageCollection:
        """
        Creates a new MessageCollection instance.

        Args:
            messages: Optional list of messages to create the collection from.
                      If not provided, an empty collection will be created.

        Returns:
            MessageCollection instance.
        """
        if isinstance(messages, dict):
            return MessageCollection(messages)
        return MessageCollection(
            {message.message_id: message for message in messages} or {}
        )

    def add_message(self, message: Message) -> MessageCollection:
        """
        Adds a message to the collection and returns a new MessageCollection
        """
        updated_messages = self.messages.copy()
        updated_messages[message.message_id] = message

        return MessageCollection(updated_messages)

    def remove_message(self, message_id: UUID) -> MessageCollection:
        """
        Removes a message from the collection and returns a new
        MessageCollection
        """
        if message_id not in self.messages:
            raise MessageNotFound(f"Message with ID: '{message_id}' not found")

        updated_messages = self.messages.copy()
        del updated_messages[message_id]

        return MessageCollection(updated_messages)

    def partial_remove(
        self,
        message_ids: List[UUID],
    ) -> Tuple[MessageCollection, Optional[List[str]]]:
        """
        Removes a list of messages from the collection and returns a new
        MessageCollection
        """
        errors = []
        updated_collection = self.messages.copy()

        for message_id in message_ids:
            try:
                updated_collection = updated_collection.remove_message(
                    message_id
                )
            except MessageNotFound:
                errors.append(f"Message with ID: '{message_id}' not found")

        return updated_collection, errors or None

    @staticmethod
    def clear_history() -> MessageCollection:
        return MessageCollection()

    def get_history(
        self,
        max_messages: Optional[int] = None,
        max_tokens: Optional[int] = None,
    ) -> List[Message]:
        """
        Returns a list of messages in the collection, ordered by timestamp,
        with the most recent message first.
        """
        result = []
        token_count = 0

        for message in reversed(self.messages.values()):
            token_count += message.total_tokens
            if (max_tokens and token_count > max_tokens) or (
                max_messages and len(result) >= max_messages
            ):
                break
            result.insert(0, message)
        return result

    @staticmethod
    def restore_history(messages: List[Message]) -> MessageCollection:
        """
        Restores the history of the collection from a list of messages.
        """
        sorted_messages = sorted(messages, key=lambda m: m.timestamp)

        return MessageCollection(
            {message.message_id: message for message in sorted_messages},
        )

    def remove_expired(
        self, timeout: Optional[int]
    ) -> Tuple[MessageCollection, Optional[List[str]]]:
        """
        Removes expired messages from the collection and returns a new
        """
        return self.message_expiration_service.remove_expired_messages(
            self, timeout
        )
