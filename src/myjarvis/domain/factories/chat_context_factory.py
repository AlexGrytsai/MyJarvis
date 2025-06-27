from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.myjarvis.domain.entities.chat_context import ChatContext
from src.myjarvis.domain.services.message_operations_service import (
    MessageOperationsService,
)
from src.myjarvis.domain.value_objects import ChatLimits, MessageCollection


@dataclass(frozen=True, slots=True)
class ChatContextFactory:
    _message_services: MessageOperationsService

    def create(
        self,
        context_id: UUID,
        agent_id: UUID,
        user_id: UUID,
        max_messages: Optional[int] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[int] = None,
    ) -> ChatContext:
        limits = ChatLimits(
            max_messages=max_messages,
            max_tokens=max_tokens,
            timeout=timeout,
        )

        return ChatContext(
            context_id=context_id,
            agent_id=agent_id,
            user_id=user_id,
            limits=limits,
            message_service=self._message_services,
        )

    def restore(
        self,
        context_id: UUID,
        agent_id: UUID,
        user_id: UUID,
        message_collection: MessageCollection,
        limits: Optional[ChatLimits] = None,
    ) -> ChatContext:
        return ChatContext(
            context_id=context_id,
            agent_id=agent_id,
            user_id=user_id,
            message_collection=message_collection,
            limits=limits,
            message_service=self._message_services,
        )
