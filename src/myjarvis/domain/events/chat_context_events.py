from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from src.myjarvis.domain.value_objects import Message


@dataclass(frozen=True)
class ChatContextEvent:
    context_id: UUID
    timestamp: datetime


@dataclass(frozen=True)
class MessageAdded(ChatContextEvent):
    message: Message


@dataclass(frozen=True)
class MessageUpdated(ChatContextEvent):
    message_id: UUID
    old_message: Message
    new_message: Message


@dataclass(frozen=True)
class MessageRemoved(ChatContextEvent):
    message_id: UUID
    removed_message: Message


@dataclass(frozen=True)
class HistoryCleared(ChatContextEvent):
    removed_messages: List[Message]


@dataclass(frozen=True)
class ExpiredMessagesRemoved(ChatContextEvent):
    expired_messages: List[Message]


@dataclass(frozen=True)
class LimitsUpdated(ChatContextEvent):
    old_max_messages: Optional[int]
    new_max_messages: Optional[int]
    old_max_tokens: Optional[int]
    new_max_tokens: Optional[int]
    old_timeout: Optional[int]
    new_timeout: Optional[int]


@dataclass(frozen=True)
class HistoryRestored(ChatContextEvent):
    restored_messages: List[Message]
