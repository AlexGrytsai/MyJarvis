from typing import List, Optional, Dict, Any
from uuid import UUID

from src.myjarvis.domain.exceptions import (
    MessageHasInvalidParentId,
    MessageNotFound,
)
from src.myjarvis.domain.services.chat_context_services import (
    ChatContextServices,
)
from src.myjarvis.domain.value_objects import (
    Message,
    MessageCollection,
    ChatLimits,
)


class MessageOperationsService:
    """
    MessageOperationsService is a service that encapsulates operations
    on message collections and ChatContexts.
    It provides methods to add, remove, and update messages while respecting
    the limits of the chat context.

    The service is responsible for verifying the correctness of the message
    operations and ensuring that the invariants of the ChatContext and Message
    collections are preserved.
    """

    slots = ("services",)

    def __init__(self, services: Optional[ChatContextServices] = None) -> None:
        self._services = services or ChatContextServices.create_default()

    def add_message(
        self,
        message: Message,
        message_collection: MessageCollection,
        limits: Optional[ChatLimits],
    ) -> MessageCollection:
        """
        Adds a message to the given message collection while respecting
        the given chat limits.

        If the message has a parent_message_id, it is checked to exist in the
        message collection. If not, a MessageHasInvalidParentId exception is
        raised.

        The message is then added to the list of messages and, if limits are
        provided, the list of messages is filtered according to the limits.

        Finally, the method returns a new MessageCollection instance with the
        updated list of messages.

        Args:
            message: The message to add to the collection.
            message_collection: The message collection to which the message is
                added.
            limits: The chat limits to apply when adding the message.

        Returns:
            A new MessageCollection instance with the updated list of messages.
        """
        if not self._check_parent_message_exists(
            message.parent_message_id, message_collection
        ):
            raise MessageHasInvalidParentId(
                "Parent ID (parent_message_id) does not exist"
            )

        messages = list(message_collection.messages.values())
        messages.append(message)

        if limits:
            messages = self._services.limits_service.apply_limits(
                messages, limits
            )

        return message_collection.create(messages)

    def update_message(
        self,
        message_id: UUID,
        message_collection: MessageCollection,
        text: Optional[str] = None,
        attachments: Optional[List[Any]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        total_tokens: Optional[int] = None,
    ) -> MessageCollection:
        """
        Updates a message in the given message collection.

        If the message does not exist in the collection, a MessageNotFound
        exception is raised.

        The message is updated with the given values and a new
        MessageCollection instance is created with the updated list of
        messages.

        Args:
            message_id: The ID of the message to update.
            message_collection: The message collection in which the message
                exists.
            text: The new text for the message.
            attachments: The new attachments for the message.
            metadata: The new metadata for the message.
            total_tokens: The new total number of tokens in the message.

        Returns:
            A new MessageCollection instance with the updated list of messages.
        """
        if not self._check_message_exists(message_id, message_collection):
            raise MessageNotFound(f"Message with ID: '{message_id}' not found")

        current_message = message_collection.messages[message_id]

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

        updated_messages = message_collection.messages.copy()
        updated_messages[updated_message.message_id] = updated_message

        return message_collection.create(updated_messages)

    def remove_message(
        self,
        message_id: UUID,
        message_collection: MessageCollection,
    ) -> MessageCollection:
        """
        Removes a message from the given message collection.

        If the message does not exist in the collection, a MessageNotFound
        exception is raised.

        Args:
            message_id: The ID of the message to remove.
            message_collection: The message collection from which the message
                                is removed.

        Returns:
            A new MessageCollection instance with the message removed.
        """
        if not self._check_message_exists(message_id, message_collection):
            raise MessageNotFound(f"Message with ID: '{message_id}' not found")

        return message_collection.remove_message(message_id)

    def remove_multiple_messages(
        self,
        message_ids: List[UUID],
        message_collection: MessageCollection,
    ) -> MessageCollection:
        """
        Removes multiple messages from the given message collection.

        This method attempts to remove each message in the provided list of
        message IDs from the message collection. If a message ID does not exist
        in the collection, it is ignored. Only existing messages are removed.

        Args:
            message_ids: A list of message IDs to remove.
            message_collection: The message collection from which the messages
                                are removed.

        Returns:
            A new MessageCollection instance with the specified messages
            removed.
        """
        checked_existing_message_ids = self._filter_existing_message_ids(
            message_ids, message_collection
        )

        if not checked_existing_message_ids:
            return message_collection

        updated_collection = message_collection
        for message_id in message_ids:
            updated_collection = updated_collection.remove_message(message_id)

        return updated_collection

    def remove_expired_messages(
        self, message_collection: MessageCollection, timeout: Optional[int]
    ) -> MessageCollection:
        """
        Removes expired messages from the given message collection.

        If the timeout is not provided (i.e., it is None), the original message
        collection is returned.

        Args:
            message_collection: The message collection from which expired
                                messages are removed.
            timeout: The timeout in seconds. If not provided, no messages are
                     removed.

        Returns:
            A new MessageCollection instance with expired messages removed.
        """
        if not timeout:
            return message_collection

        return self._services.expiration_service.remove_expired_messages(
            message_collection, timeout
        )

    @staticmethod
    def _check_parent_message_exists(
        parent_message_id: UUID,
        message_collection: MessageCollection,
    ) -> bool:
        return not parent_message_id or any(
            m.message_id == parent_message_id
            for m in message_collection.messages.values()
        )

    @staticmethod
    def _check_message_exists(
        message_id: UUID,
        message_collection: MessageCollection,
    ) -> bool:
        return message_id in message_collection.messages

    def _filter_existing_message_ids(
        self,
        message_ids: List[UUID],
        message_collection: MessageCollection,
    ) -> List[UUID]:
        filtered_message_ids = []
        filtered_message_ids.extend(
            message_id
            for message_id in message_ids
            if self._check_message_exists(message_id, message_collection)
        )
        return filtered_message_ids
