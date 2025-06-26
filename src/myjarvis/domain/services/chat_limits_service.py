from dataclasses import dataclass
from typing import List

from src.myjarvis.domain.value_objects import Message, ChatLimits


@dataclass(slots=True)
class ChatLimitsService:
    """
    This class is responsible for enforcing chat limits.

    It provides methods to limit the number of messages and the total number of
    tokens in a chat session. This is useful for preventing abuse and ensuring
    that the chatbot is not flooded with messages.

    The class takes a ChatLimits object in its constructor, which specifies the
    limits to enforce. It then provides methods to apply these limits to a list
    of messages.

    The class is designed to be used as a simple, stateless service.
    """

    def apply_limits(
        self,
        messages: List[Message],
        limits: ChatLimits,
    ) -> List[Message]:
        """
        Applies the specified chat limits to the provided list of messages.

        This method enforces both the maximum number of messages and the
        maximum number of tokens as defined by the given ChatLimits object.
        It returns a new list of messages that comply with these limits.

        Args:
            messages (List[Message]): The list of messages to be limited.
            limits (ChatLimits): The chat limits to enforce.

        Returns:
            List[Message]: A list of messages adhering to the specified limits.
        """
        return self._enforce_max_tokens(
            self._enforce_max_messages(messages, limits), limits
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
        total_tokens = sum(message.total_tokens for message in messages)
        if limits.max_tokens is None or total_tokens <= limits.max_tokens:
            return messages

        sorted_messages = sorted(
            messages, key=lambda m: m.timestamp, reverse=True
        )

        kept_messages = []
        accumulated_tokens = 0

        for message in sorted_messages:
            if accumulated_tokens + message.total_tokens > limits.max_tokens:
                break
            kept_messages.append(message)
            accumulated_tokens += message.total_tokens

        return kept_messages
