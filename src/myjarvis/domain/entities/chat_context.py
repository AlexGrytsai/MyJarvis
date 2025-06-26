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
from src.myjarvis.domain.services import ChatContextLimitsService
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
    limits: Optional[ChatLimits] = None
    chat_limits_service: ChatContextLimitsService = field(
        default_factory=ChatContextLimitsService
    )
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        self._validate_required_fields()

    @classmethod
    def create(
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
            limits=ChatLimits(
                max_messages=max_messages,
                max_tokens=max_tokens,
                timeout=timeout,
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

        messages = list(self.message_collection.messages.values())
        messages.append(message)

        updated_message_collection = self.message_collection.create(
            self.chat_limits_service.apply_limits(
                messages=messages, limits=self.limits
            )
        )
        return self._create_updated_context(
            message_collection=updated_message_collection
        )

    def get_history(
        self,
        max_messages: Optional[int] = None,
        max_tokens: Optional[int] = None,
    ) -> List[Message]:
        return self.message_collection.get_history(
            max_messages=max_messages, max_tokens=max_tokens
        )

    def update_message(
        self,
        message_id: UUID,
        text: Optional[str] = None,
        attachments: Optional[List[Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        total_tokens: Optional[int] = None,
    ) -> Message:
        if message_id not in self.message_collection.messages:
            raise MessageNotFound(f"Message with ID: '{message_id}' not found")

        current_message = self.message_collection.messages[message_id]

        updated_message = Message(
            message_id=current_message.message_id,
            sender=current_message.sender,
            text=text if text is not None else current_message.text,
            timestamp=current_message.timestamp,
            role=current_message.role,
            parent_message_id=current_message.parent_message_id,
            attachments=(
                attachments
                if attachments is not None
                else current_message.attachments
            ),
            metadata=(
                metadata if metadata is not None else current_message.metadata
            ),
            total_tokens=(
                total_tokens
                if total_tokens is not None
                else current_message.total_tokens
            ),
        )

        updated_messages = self.message_collection.messages.copy()
        updated_messages[updated_message.message_id] = updated_message

        return self._create_updated_context(
            message_collection=MessageCollection(
                updated_messages, self.message_collection.limits
            )
        ).message_collection.messages[message_id]

    def remove_message(self, message_id: UUID) -> ChatContext:
        updated_messages = self.message_collection.remove_message(message_id)
        return self._create_updated_context(
            message_collection=updated_messages
        )

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
            message_collection=MessageCollection(
                self.message_collection.messages, new_limits
            ),
        )

    def _create_updated_context(self, **kwargs) -> ChatContext:
        return ChatContext(
            context_id=self.context_id,
            agent_id=self.agent_id,
            user_id=self.user_id,
            created_at=self.created_at,
            limits=kwargs.get("limits", self.limits),
            message_collection=kwargs.get(
                "message_collection", self.message_collection
            ),
            updated_at=datetime.now(),
        )

    def _validate_required_fields(self) -> None:
        if not self.agent_id:
            raise AgentIdRequired("Agent ID (agent_id) required")
        if not self.user_id:
            raise UserIdRequired("User ID (user_id) required")
