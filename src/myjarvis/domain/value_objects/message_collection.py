from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from uuid import UUID

from src.myjarvis.domain.exceptions import MessageNotFound
from src.myjarvis.domain.value_objects import Message
from src.myjarvis.domain.value_objects.chat_limits import ChatLimits


@dataclass(frozen=True, slots=True)
class MessageCollection:
    """
    Value object that stores a collection of messages, along with their limits.

    Stores a mapping of message IDs to Message objects, as well as a ChatLimits
    object that describes the limits of the messages in the collection.

    Also provides methods for adding and removing messages, which return new
    MessageCollection objects with the updated messages and limits.
    """

    messages: Dict[UUID, Message] = field(default_factory=dict)
    limits: ChatLimits = field(default_factory=ChatLimits)

    def __post_init__(self):
        messages_with_limits = self._enforce_limits(
            messages=list(self.messages.values()),
            limits=self.limits,
        )
        object.__setattr__(
            self, "messages", {m.message_id: m for m in messages_with_limits}
        )

    @property
    def total_tokens(self) -> int:
        """Returns the total number of tokens in the collection."""
        return sum(message.total_tokens for message in self.messages.values())

    @property
    def total_messages(self) -> int:
        """Returns the total number of messages in the collection."""
        return len(self.messages)

    def add_message(self, message: Message) -> MessageCollection:
        """
        Adds a message to the collection and returns a new MessageCollection
        """
        updated_messages = self.messages.copy()
        updated_messages[message.message_id] = message

        return MessageCollection(updated_messages, self.limits)

    def remove_message(self, message_id: UUID) -> MessageCollection:
        """
        Removes a message from the collection and returns a new
        MessageCollection
        """
        if message_id not in self.messages:
            raise MessageNotFound(f"Message with ID: '{message_id}' not found")

        updated_messages = self.messages.copy()
        del updated_messages[message_id]

        return MessageCollection(updated_messages, self.limits)

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

    def clear_history(self) -> MessageCollection:
        return MessageCollection(limits=self.limits)

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

    def restore_history(self, messages: List[Message]) -> MessageCollection:
        """
        Restores the history of the collection from a list of messages.
        """
        sorted_messages = sorted(messages, key=lambda m: m.timestamp)

        return MessageCollection(
            {message.message_id: message for message in sorted_messages},
            self.limits,
        )

    def remove_expired(
        self, timeout: Optional[int]
    ) -> Tuple[MessageCollection, Optional[List[str]]]:
        """
        Removes expired messages from the collection and returns a new
        """
        if not timeout:
            return self, None

        now = datetime.now()
        ids_to_remove = [
            message_id
            for message_id, message in self.messages.items()
            if (now - message.timestamp).total_seconds() > timeout
        ]

        return self.partial_remove(ids_to_remove)

    def _enforce_limits(
        self,
        messages: List[Message],
        limits: ChatLimits,
    ) -> List[Message]:
        """
        Enforces the limits on the messages in the collection and returns a new
        list of messages.
        """
        return self._enforce_max_tokens(
            messages=self._enforce_max_messages(messages, limits),
            limits=limits,
        )

    @staticmethod
    def _enforce_max_messages(
        messages: List[Message], limits: ChatLimits
    ) -> List[Message]:
        """
        Enforces the maximum number of messages in the collection and returns a
        new list of messages.
        """
        if limits.max_messages is None or len(messages) <= limits.max_messages:
            return messages

        return messages[-limits.max_messages :]

    def _enforce_max_tokens(
        self,
        messages: List[Message],
        limits: ChatLimits,
    ) -> List[Message]:
        """
        Enforces the maximum number of tokens in the collection and returns
        a new list of messages.
        """
        if limits.max_tokens is None or self.total_tokens <= limits.max_tokens:
            return messages

        sorted_messages = sorted(
            messages, key=lambda m: m.timestamp, reverse=True
        )

        kept_messages = []
        accumulated_tokens = 0

        for message in sorted_messages:
            if (
                accumulated_tokens + message.total_tokens
                > self.limits.max_tokens
            ):
                break
            kept_messages.append(message)
            accumulated_tokens += message.total_tokens

        return kept_messages
