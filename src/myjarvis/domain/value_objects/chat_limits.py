from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.myjarvis.domain.exceptions import (
    MaxTokensNotValid,
    MaxMessagesNotValid,
    TimeoutNotValid,
)


@dataclass(frozen=True, slots=True)
class ChatLimits:
    max_messages: Optional[int] = None
    max_tokens: Optional[int] = None
    timeout: Optional[int] = None

    def __post_init__(self):
        if self.max_messages is not None and (
            not isinstance(self.max_messages, int) or self.max_messages <= 0
        ):
            raise MaxMessagesNotValid(
                f"Maximum messages must be positive int or None. "
                f"Got: {self.max_messages}"
            )
        if self.max_tokens is not None and (
            not isinstance(self.max_tokens, int) or self.max_tokens <= 0
        ):
            raise MaxTokensNotValid(
                "Maximum tokens must be positive int or None"
            )
        if self.timeout is not None and (
            not isinstance(self.timeout, int) or self.timeout <= 0
        ):
            raise TimeoutNotValid("Timeout must be positive int or None")

    @classmethod
    def create(
        cls,
        max_messages: Optional[int] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[int] = None,
    ):
        return cls(
            max_messages=max_messages,
            max_tokens=max_tokens,
            timeout=timeout,
        )

    def update_limits(
        self,
        old_limits: Optional[ChatLimits] = None,
        max_messages: Optional[int] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[int] = None,
    ) -> ChatLimits:
        if not old_limits:
            return self.create(max_messages, max_tokens, timeout)
        return self.create(
            max_messages=(
                max_messages
                if max_messages is not None
                else old_limits.max_messages
            ),
            max_tokens=(
                max_tokens if max_tokens is not None else old_limits.max_tokens
            ),
            timeout=timeout if timeout is not None else old_limits.timeout,
        )
