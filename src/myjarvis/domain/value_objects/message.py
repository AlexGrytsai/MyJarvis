from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any, Dict, List, Union
from uuid import UUID

from src.myjarvis.domain.exceptions import (
    MessageCouldNotBeEmpty,
    MessageWithoutId,
    MessageMetaDataWrongFormat,
    MessageTooLong,
    AttachmentsToMessageInWrongFormat,
    WrongIdType,
    WrongDatatimeType,
    InvalidMessageRole,
)
from src.myjarvis.domain.value_objects.message_role import MessageRole


@dataclass(frozen=True, slots=True)
class Message:
    """
    Message value object represents a single message in a conversation.
    It has a unique identifier, sender's ID, text of the message, timestamp
    of when the message was sent, the role of the sender, and an optional
    ID of the parent message. It also has a list of attachments, a dictionary
    of additional metadata, and an optional maximum text length.
    """

    message_id: UUID
    sender: Union[str, UUID]
    text: str = ""
    timestamp: datetime = field(default_factory=datetime.now)
    role: MessageRole = MessageRole.USER
    parent_message_id: Optional[UUID] = None
    attachments: List[Any] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    max_text_length: Optional[int] = None
    total_tokens: int = 0

    def __post_init__(self):
        if not isinstance(self.message_id, UUID):
            raise MessageWithoutId("message_id must be UUID")
        if not isinstance(self.text, str) or not self.text:
            raise MessageCouldNotBeEmpty("Text must be non-empty string")
        if self.max_text_length and len(self.text) > self.max_text_length:
            raise MessageTooLong(
                f"Text too long. Max length: {self.max_text_length}"
            )
        if self.parent_message_id and not isinstance(
            self.parent_message_id, UUID
        ):
            raise WrongIdType("Parent_message_id must be UUID")
        if not isinstance(self.timestamp, datetime):
            raise WrongDatatimeType("Timestamp must be datetime")
        if not isinstance(self.role, MessageRole):
            raise InvalidMessageRole("Role must be MessageRole")
        if not isinstance(self.attachments, list):
            raise AttachmentsToMessageInWrongFormat("Attachments must be list")
        if not isinstance(self.metadata, dict):
            raise MessageMetaDataWrongFormat("metadata must be dict")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Message):
            return False
        return self.message_id == other.message_id

    def __hash__(self) -> int:
        return hash(self.message_id)
