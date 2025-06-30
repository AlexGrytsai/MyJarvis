from __future__ import annotations

from datetime import datetime
from typing import List, Optional, Dict, Any, TypeAlias
from uuid import UUID

from src.myjarvis.domain.exceptions import (
    AgentIdRequired,
    UserIdRequired,
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
        message_collection: Optional[MessageCollection] = None,
        limits: ChatLimits = ChatLimits(),
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self._context_id = context_id
        self._agent_id = agent_id
        self._user_id = user_id
        self._message_collection = message_collection or MessageCollection()
        self._message_service = message_service
        self._limits = limits
        self._created_at = created_at or datetime.now()
        self._updated_at = updated_at or datetime.now()

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
        message_service: MessageOperationsService,
        message_collection: Optional[MessageCollection] = None,
        max_messages: Optional[int] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[int] = None,
        created_at: Optional[datetime] = None,
    ) -> ChatContext:
        return cls(
            context_id=context_id,
            agent_id=agent_id,
            user_id=user_id,
            message_service=message_service,
            message_collection=message_collection or MessageCollection(),
            limits=ChatLimits(
                max_messages=max_messages,
                max_tokens=max_tokens,
                timeout=timeout,
            ),
            created_at=created_at or datetime.now(),
        )

    def add_message(self, message: Message) -> ChatContext:
        return self._create_updated_context(
            message_collection=self._message_service.add_message(
                message=message,
                message_collection=self._message_collection,
                limits=self._limits,
            )
        )

    def get_history(
        self,
        max_messages: Optional[int] = None,
        max_tokens: Optional[int] = None,
    ) -> List[Message]:
        return self._message_collection.get_history(
            max_messages=max_messages, max_tokens=max_tokens
        )

    def update_message(
        self,
        message_id: UUID,
        text: Optional[str] = None,
        attachments: Optional[List[Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        total_tokens: Optional[int] = None,
    ) -> Optional[Message]:
        updated_message_collection = self._message_service.update_message(
            message_id=message_id,
            message_collection=self._message_collection,
            text=text,
            attachments=attachments,
            metadata=metadata,
            total_tokens=total_tokens,
        )

        return self._create_updated_context(
            message_collection=updated_message_collection
        )._message_collection.get_message(message_id)

    def remove_message(self, message_id: UUID) -> ChatContext:
        return self._create_updated_context(
            message_collection=self._message_collection.remove_message(
                message_id
            )
        )

    def clear_history(self) -> ChatContext:
        return self._create_updated_context(
            message_collection=self._message_collection.clear_history()
        )

    def remove_expired(self) -> ChatContext:
        if not self._limits or not self._limits.timeout:
            return self

        message_collection = self._message_service.remove_expired_messages(
            message_collection=self._message_collection,
            timeout=self._limits.timeout,
        )

        return self._create_updated_context(
            message_collection=message_collection
        )

    def partial_remove(
        self,
        message_ids: List[UUID],
    ) -> ChatContext:
        new_message_collection = self._message_collection.partial_remove(
            message_ids
        )
        return self._create_updated_context(
            message_collection=new_message_collection
        )

    def restore_history(self, messages: List[Message]) -> ChatContext:
        sorted_messages = sorted(messages, key=lambda m: m.timestamp)
        return self._create_updated_context(
            message_collection=self._message_collection.restore_history(
                sorted_messages
            )
        )

    def update_limits(
        self,
        max_messages: Optional[int] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[int] = None,
    ) -> ChatContext:

        return self._create_updated_context(
            limits=self._limits.update_limits(
                old_limits=self._limits,
                max_messages=max_messages,
                max_tokens=max_tokens,
                timeout=timeout,
            ),
        )

    def _create_updated_context(
        self,
        message_collection: Optional[MessageCollection] = None,
        limits: Optional[ChatLimits] = None,
        messages: Optional[List[Message]] = None,
    ) -> ChatContext:
        if not message_collection and messages:
            message_collection = self._message_collection.create(
                messages=messages
            )
        return ChatContext(
            context_id=self.context_id,
            agent_id=self.agent_id,
            user_id=self.user_id,
            created_at=self._created_at,
            limits=limits or self._limits,
            message_collection=message_collection or self._message_collection,
            message_service=self._message_service,
            updated_at=datetime.now(),
        )

    def _validate_required_fields(self) -> None:
        if not self.agent_id:
            raise AgentIdRequired("Agent ID (agent_id) required")
        if not self.user_id:
            raise UserIdRequired("User ID (user_id) required")
