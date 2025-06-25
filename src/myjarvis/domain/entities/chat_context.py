from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any, Union
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
    UnexpectedException,
    MessageNotFound,
)
from src.myjarvis.domain.value_objects import Message


@dataclass
class ChatContext:
    context_id: UUID
    agent_id: Union[str, UUID]
    user_id: Union[str, UUID]
    messages: Dict[UUID, Message] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    timeout: Optional[int] = None
    max_messages: Optional[int] = None
    max_tokens: Optional[int] = None
    total_tokens: int = 0

    def __post_init__(self):
        self._validate()
        self._enforce_limits()

    def add_message(self, message: Message) -> ChatContext:
        if message.parent_message_id and all(
            m.message_id != message.parent_message_id
            for m in self.messages.values()
        ):
            raise MessageHasInvalidParentId(
                "Parent ID (parent_message_id) does not exist"
            )
        self.messages[message.message_id] = message
        self.total_tokens += message.total_tokens
        self._enforce_limits()
        self.updated_at = datetime.now()
        return self

    def get_history(
        self,
        limit: Optional[int] = None,
        max_tokens: Optional[int] = None,
    ) -> List[Message]:
        result = []
        token_count = 0
        for message in reversed(self.messages.values()):
            token_count += message.total_tokens
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
        total_tokens: Optional[int] = None,
    ) -> Message:
        message_for_update = self.messages.get(message_id)
        if not message_for_update:
            raise MessageNotFound(f"Message with ID: '{message_id}' not found")

        updated_message = Message(
            message_id=message_for_update.message_id,
            sender=message_for_update.sender,
            text=text if text is not None else message_for_update.text,
            timestamp=message_for_update.timestamp,
            role=message_for_update.role,
            parent_message_id=message_for_update.parent_message_id,
            attachments=(
                attachments
                if attachments is not None
                else message_for_update.attachments
            ),
            metadata=(
                metadata
                if metadata is not None
                else message_for_update.metadata
            ),
            total_tokens=(
                total_tokens
                if total_tokens is not None
                else message_for_update.total_tokens
            ),
        )
        self.messages[message_id] = updated_message

        self._enforce_max_tokens()

        self.updated_at = datetime.now()

        return updated_message

    def remove_message(self, message_id: UUID) -> bool:
        if not self.messages.get(message_id):
            raise MessageNotFound(f"Message with ID: '{message_id}' not found")
        self.total_tokens -= self.messages[message_id].total_tokens
        del self.messages[message_id]

        self.updated_at = datetime.now()

        return True

    def clear_history(self):
        self.messages.clear()
        self.total_tokens = 0
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

    def _enforce_limits(self) -> None:
        self._enforce_max_messages()
        self._enforce_max_tokens()

    def _enforce_max_messages(self) -> None:
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages :]

    def _enforce_max_tokens(self) -> None:
        while self.total_tokens > self.max_tokens:
            if self.messages:
                message_id_to_remove = list(self.messages.keys())[0]
                self.total_tokens -= self.messages[
                    message_id_to_remove
                ].total_tokens
                del self.messages[message_id_to_remove]
            raise UnexpectedException(
                f"Total tokens is not empty ({self.total_tokens}), "
                f"but messages list is empty"
            )

    def _validate(self) -> None:
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
