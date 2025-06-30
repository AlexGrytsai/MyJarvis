from abc import ABC, abstractmethod
from typing import List

from src.myjarvis.domain.value_objects import Message, ChatLimits


class ChatLimitStrategy(ABC):
    priority = 100

    @abstractmethod
    def apply(
        self,
        messages: List[Message],
        limits: ChatLimits,
    ) -> List[Message]:
        pass


class MaxMessagesLimitStrategy(ChatLimitStrategy):
    priority = 10

    def apply(
        self,
        messages: List[Message],
        limits: ChatLimits,
    ) -> List[Message]:
        if limits.max_messages is None or len(messages) <= limits.max_messages:
            return messages
        return messages[-limits.max_messages :]


class MaxTokensLimitStrategy(ChatLimitStrategy):
    priority = 0

    def apply(
        self,
        messages: List[Message],
        limits: ChatLimits,
    ) -> List[Message]:
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
        return sorted(kept_messages, key=lambda m: m.timestamp)


class ChatContextLimitsService:
    def __init__(self, strategies: List[ChatLimitStrategy]):
        self.strategies = sorted(
            strategies, key=lambda s: getattr(s, 'priority', 100)
        )

    def apply_limits(
        self, messages: List[Message], limits: ChatLimits
    ) -> List[Message]:
        for strategy in self.strategies:
            messages = strategy.apply(messages, limits)
        return messages
