from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any, Union, Deque
from uuid import UUID

from src.myjarvis.domain.exceptions import (
    AgentIdRequired,
    UserIdRequired,
    ContextIdInvalidFormat,
    MaxTokensNotValid,
    MaxMessagesNotValid,
    TimeoutNotValid,
    MessagesListNotValid,
    MessageHasInvalidParentId,
)
from src.myjarvis.domain.value_objects import Message


@dataclass
class ChatContext:
    context_id: UUID
    agent_id: Union[str, UUID]
    user_id: Union[str, UUID]
    messages: Deque[Message] = field(default_factory=deque)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    timeout: Optional[int] = None
    max_messages: Optional[int] = None
    max_tokens: Optional[int] = None
    total_tokens: int = 0

    def __post_init__(self):
        self._validate()
        self._enforce_limits()

    def add_message(self, message: Message):
        if message.parent_message_id and all(
            m.message_id != message.parent_message_id for m in self.messages
        ):
            raise MessageHasInvalidParentId(
                "Parent ID (parent_message_id) does not exist"
            )
        self.messages.append(message)
        self.updated_at = datetime.now()
        self._enforce_limits()

    def get_history(
        self, limit: Optional[int] = None, max_tokens: Optional[int] = None
    ) -> List[Message]:
        result = []
        token_count = 0
        for message in reversed(self.messages):
            token_count += len(message.text)
            if (max_tokens and token_count > max_tokens) or (
                limit and len(result) >= limit
            ):
                break
            result.insert(0, message)
        return result

    def update_message(
        self,
        message_id: UUID,
        text: Optional[str] = None,
        attachments: Optional[List[Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        updated = False
        new_messages = []
        for m in self.messages:
            if m.message_id == message_id:
                new_m = Message(
                    message_id=m.message_id,
                    sender=m.sender,
                    text=text if text is not None else m.text,
                    timestamp=m.timestamp,
                    role=m.role,
                    parent_message_id=m.parent_message_id,
                    attachments=(
                        attachments
                        if attachments is not None
                        else m.attachments
                    ),
                    metadata=metadata if metadata is not None else m.metadata,
                )
                new_messages.append(new_m)
                updated = True
            else:
                new_messages.append(m)
        if not updated:
            raise ValueError("Message not found")
        self.messages = new_messages
        self.updated_at = datetime.now()

    def remove_message(self, message_id: UUID):
        self.messages = [
            m for m in self.messages if m.message_id != message_id
        ]
        self.updated_at = datetime.now()

    def clear_history(self):
        self.messages = []
        self.updated_at = datetime.now()

    def remove_expired(self):
        if not self.timeout:
            return
        now = datetime.now()
        self.messages = [
            m
            for m in self.messages
            if (now - m.timestamp).total_seconds() <= self.timeout
        ]
        self.updated_at = datetime.now()

    def partial_remove(self, message_ids: List[UUID]):
        self.messages = [
            m for m in self.messages if m.message_id not in message_ids
        ]
        self.updated_at = datetime.now()

    def restore_history(self, messages: List[Message]):
        self.messages = messages
        self.messages.sort(key=lambda m: m.timestamp)
        self.updated_at = datetime.now()
        self._enforce_limits()

    def _enforce_limits(self):
        self._enforce_max_messages()
        self._enforce_max_tokens()

    def _enforce_max_messages(self):
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages :]

    def _enforce_max_tokens(self):
        token_sum = 0
        result = []
        for message in reversed(self.messages):
            token_sum += message.total_tokens
            if token_sum > self.max_tokens:
                break
            result.insert(0, message)
        self.messages = result

    def _validate(self):
        if not self.agent_id:
            raise AgentIdRequired("Agent ID (agent_id) required")
        if not self.user_id:
            raise UserIdRequired("User ID (user_id) required")
        if not isinstance(self.context_id, UUID):
            raise ContextIdInvalidFormat(
                "Context ID (context_id) must be UUID"
            )
        if not isinstance(self.max_messages, int):
            raise MaxMessagesNotValid(
                f"Maximum messages (max_messages) must be positive int "
                f"or None. Got: {self.max_messages}, "
                f"type: {type(self.max_messages)}"
            )
        if self.max_messages <= 0:
            raise MaxMessagesNotValid(
                f"Maximum messages (max_messages) must be positive int "
                f"or None. Got: {self.max_messages}"
            )
        if not isinstance(self.max_tokens, int) or self.max_tokens <= 0:
            raise MaxTokensNotValid(
                "Maximum tokens (max_tokens) must be positive int or None"
            )
        if self.timeout is not None and (
            not isinstance(self.timeout, int) or self.timeout <= 0
        ):
            raise TimeoutNotValid("Timeout must be positive int or None")
        if not isinstance(self.messages, list):
            raise MessagesListNotValid(
                f"Messages must be list. Got: {type(self.messages)}"
            )
