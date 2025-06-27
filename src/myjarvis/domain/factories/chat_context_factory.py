from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID

from src.myjarvis.domain.entities.chat_context import ChatContext
from src.myjarvis.domain.services.message_operations_service import (
    MessageOperationsService,
)
from src.myjarvis.domain.value_objects import ChatLimits, MessageCollection


@dataclass(frozen=True, slots=True)
class ChatContextFactory:
    _message_operations: MessageOperationsService

    def create(
        self,
        context_id: UUID,
        agent_id: UUID,
        user_id: UUID,
        max_messages: Optional[int] = None,
        max_tokens: Optional[int] = None,
        timeout: Optional[int] = None,
    ) -> Result[ChatContext, str]:
        validation_result = self._validator.validate_required_fields(
            agent_id, user_id
        )
        if is_failure(validation_result):
            return validation_result

        limits = ChatLimits(
            max_messages=max_messages,
            max_tokens=max_tokens,
            timeout=timeout,
        )

        context = ChatContext(
            context_id=context_id,
            agent_id=agent_id,
            user_id=user_id,
            message_collection=MessageCollection(),
            limits=limits,
            services=self._services,
            validator=self._validator,
            message_operations=self._message_operations,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return success(context)

    def restore(
        self,
        context_id: UUID,
        agent_id: UUID,
        user_id: UUID,
        message_collection: MessageCollection,
        limits: Optional[ChatLimits] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> Result[ChatContext, str]:
        validation_result = self._validator.validate_required_fields(
            agent_id, user_id
        )
        if is_failure(validation_result):
            return validation_result

        context = ChatContext(
            context_id=context_id,
            agent_id=agent_id,
            user_id=user_id,
            message_collection=message_collection,
            limits=limits,
            services=self._services,
            validator=self._validator,
            message_operations=self._message_operations,
            created_at=created_at or datetime.now(),
            updated_at=updated_at or datetime.now(),
        )

        return success(context)
