from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple
from uuid import UUID

from src.myjarvis.domain.exceptions import (
    AgentIdRequired,
    UserIdRequired,
    MessageHasInvalidParentId,
    MessageNotFound,
)
from src.myjarvis.domain.value_objects import (
    Message,
    ChatLimits,
    MessageCollection,
)


@dataclass
class ChatContext:
    context_id: UUID
    agent_id: UUID
    user_id: UUID
    message_collection: MessageCollection = field(
        default_factory=MessageCollection
    )
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        self._validate_required_fields()

    @classmethod
    def create_with_limits(
        cls,
        context_id: UUID,
        agent_id: UUID,
        user_id: UUID,
        max_messages: Optional[int] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[int] = None,
    ) -> ChatContext:
        return cls(
            context_id=context_id,
            agent_id=agent_id,
            user_id=user_id,
            message_collection=MessageCollection(
                limits=ChatLimits(
                    max_messages=max_messages,
                    max_tokens=max_tokens,
                    timeout=timeout,
                )
            ),
        )

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

    def remove_expired(self) -> Tuple[Dict[UUID, Message], Optional[List]]:
        if not self.timeout:
            return self.messages, None
        now = datetime.now()

        ids_to_remove = [
            message_id
            for message_id in self.messages.keys()
            if (now - self.messages[message_id].timestamp).total_seconds()
            > self.timeout
        ]

        _, errors = self.partial_remove(ids_to_remove)
        self.updated_at = datetime.now()

        return self.messages, errors

    def partial_remove(
        self,
        message_ids: List[UUID],
    ) -> Tuple[Dict[UUID, Message], Optional[List]]:
        errors = []
        for message_id in message_ids:
            try:
                self.remove_message(message_id)
            except MessageNotFound:
                errors.append(f"Message with ID: '{message_id}' not found")
        self.updated_at = datetime.now()

        return self.messages, errors

    def restore_history(self, messages: List[Message]) -> Dict[UUID, Message]:
        sorted_messages = sorted(messages, key=lambda m: m.timestamp)
        self.messages = {
            message.message_id: message for message in sorted_messages
        }

        self.updated_at = datetime.now()

        return self.messages

    def update_limits(
        self,
        max_messages: Optional[int] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[int] = None,
    ) -> ChatContext:
        new_limits = ChatLimits(
            max_messages=(
                max_messages
                if max_messages is not None
                else self.message_collection.limits.max_messages
            ),
            max_tokens=(
                max_tokens
                if max_tokens is not None
                else self.message_collection.limits.max_tokens
            ),
            timeout=(
                timeout
                if timeout is not None
                else self.message_collection.limits.timeout
            ),
        )

        return self._create_updated_context(
            limits=new_limits,
            message_collection=MessageCollection(
                self.message_collection.messages, new_limits
            ),
        )

    def _create_updated_context(self, **kwargs) -> ChatContext:
        return ChatContext(
            context_id=self.context_id,
            agent_id=self.agent_id,
            user_id=self.user_id,
            limits=kwargs.get("limits", self.limits),
            created_at=self.created_at,
        )

    def _validate_required_fields(self) -> None:
        if not self.agent_id:
            raise AgentIdRequired("Agent ID (agent_id) required")
        if not self.user_id:
            raise UserIdRequired("User ID (user_id) required")
