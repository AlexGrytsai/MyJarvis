from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict, Any, Tuple, TypeAlias
from uuid import UUID

from src.myjarvis.domain.exceptions import (
    AgentIdRequired,
    UserIdRequired,
    MessageHasInvalidParentId,
    MessageNotFound,
)
from src.myjarvis.domain.services import MessageOperationsService
from src.myjarvis.domain.value_objects import (
    Message,
    ChatLimits,
    MessageCollection,
)

ErrorsMessages: TypeAlias = Optional[List[str]]


class ChatContext:
    def __init__(
        self,
        context_id: UUID,
        agent_id: UUID,
        user_id: UUID,
        message_service: MessageOperationsService,
        message_collection: MessageCollection = MessageCollection(),
        limits: Optional[ChatLimits] = None,
    ):
        self._context_id = context_id
        self._agent_id = agent_id
        self._user_id = user_id
        self._message_collection = message_collection
        self._message_service = message_service
        self._limits = limits
        self._created_at = datetime.now()
        self._updated_at = datetime.now()

    @property
    def context_id(self) -> UUID:
        return self._context_id

    @property
    def agent_id(self) -> UUID:
        return self._agent_id

    @property
    def user_id(self) -> UUID:
        return self._user_id

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def updated_at(self) -> datetime:
        return self._updated_at

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
            for m in self.message_collection.messages.values()
        ):
            raise MessageHasInvalidParentId(
                "Parent ID (parent_message_id) does not exist"
            )

        messages = list(self.message_collection.messages.values())
        messages.append(message)

        return self._create_updated_context(messages=messages)

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
            messages=list(updated_messages.values())
        ).message_collection.messages[message_id]

    def remove_message(self, message_id: UUID) -> ChatContext:
        return self._create_updated_context(
            message_collection=self.message_collection.remove_message(
                message_id
            )
        )

    def clear_history(self) -> ChatContext:
        return self._create_updated_context(
            message_collection=self.message_collection.clear_history()
        )

    def remove_expired(self) -> Tuple[ChatContext, ErrorsMessages]:
        if not self.limits.timeout:
            return self, None

        message_collection, errors = (
            self.message_expiration_service.remove_expired_messages(
                messages_collection=self.message_collection,
                timeout=self.limits.timeout,
            )
        )
        self._create_updated_context(message_collection=message_collection)

        return self, errors

    def partial_remove(
        self,
        message_ids: List[UUID],
    ) -> Tuple[ChatContext, ErrorsMessages]:
        errors = []
        for message_id in message_ids:
            try:
                self.remove_message(message_id)
            except MessageNotFound:
                errors.append(f"Message with ID: '{message_id}' not found")

        return self, errors

    def restore_history(self, messages: List[Message]) -> ChatContext:
        sorted_messages = sorted(messages, key=lambda m: m.timestamp)
        self._create_updated_context(
            message_collection=self.message_collection.restore_history(
                sorted_messages
            )
        )

        return self

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
                else self.limits.max_messages
            ),
            max_tokens=(
                max_tokens
                if max_tokens is not None
                else self.limits.max_tokens
            ),
            timeout=(timeout if timeout is not None else self.limits.timeout),
        )

        return self._create_updated_context(
            limits=new_limits,
        )

    def _create_updated_context(
        self,
        message_collection: Optional[MessageCollection] = None,
        limits: Optional[ChatLimits] = None,
        messages: Optional[List[Message]] = None,
    ) -> ChatContext:
        if messages and not message_collection:
            check_limits = self.chat_limits_service.apply_limits(
                messages=messages, limits=self.limits
            )
            message_collection = self.message_collection.create(check_limits)
        return ChatContext(
            context_id=self.context_id,
            agent_id=self.agent_id,
            user_id=self.user_id,
            created_at=self.created_at,
            limits=limits or self.limits,
            message_collection=message_collection or self.message_collection,
            updated_at=datetime.now(),
        )

    def _validate_required_fields(self) -> None:
        if not self.agent_id:
            raise AgentIdRequired("Agent ID (agent_id) required")
        if not self.user_id:
            raise UserIdRequired("User ID (user_id) required")
