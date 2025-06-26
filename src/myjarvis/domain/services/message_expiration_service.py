from datetime import datetime
from typing import Tuple, Optional, List, TypeAlias

from src.myjarvis.domain.value_objects import MessageCollection, Message

Errors: TypeAlias = Optional[List[str]]


class MessageExpirationService:
    """
    This service is responsible for removing expired messages from
    a collection.

    It defines a domain logic for checking if a message is expired based
    on its timestamp and a given timeout value. The expiration check is done
    by comparing the difference between the current time and the message's
    timestamp with the given timeout value.
    """

    def remove_expired_messages(
        self, messages_collection: MessageCollection, timeout: int
    ) -> Tuple[MessageCollection, Errors]:
        """
        Removes expired messages from the collection and returns a new
        """
        if not timeout:
            return messages_collection, None

        ids_to_remove = [
            message_id
            for message_id, message in messages_collection.messages.items()
            if self._is_message_expired(message, timeout)
        ]

        return messages_collection.partial_remove(ids_to_remove)

    @staticmethod
    def _is_message_expired(message: Message, timeout: int) -> bool:
        return (datetime.now() - message.timestamp).total_seconds() > timeout
