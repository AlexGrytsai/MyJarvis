"""
This module provides a cache implementation using Redis.

It is primarily used for caching chat contexts to maintain conversation history
without repeatedly querying the main database. This improves performance and
reduces latency in chat interactions.

The implementation should provide a simple key-value store interface with methods
for setting, getting, and deleting cache entries. It will use the `redis-py`
library for asynchronous communication with a Redis server.

Example Implementation:

import json
from typing import Any
from redis.asyncio import Redis as AsyncRedis
from myjarvis.domain.entities.chat_context import ChatContext

class RedisCache:
    def __init__(self, redis_client: AsyncRedis):
        self._client = redis_client

    async def get_chat_context(self, agent_id: str) -> ChatContext | None:
        Retrieves a chat context from the cache.

        Args:
            agent_id (str): The unique identifier for the AI agent.

        Returns:
            ChatContext | None: The deserialized ChatContext object if found,
                                otherwise None.
        cached_context = await self._client.get(f"chat_context:{agent_id}")
        if cached_context:
            return ChatContext(**json.loads(cached_context))
        return None

    async def set_chat_context(self, context: ChatContext) -> None:
        Saves a chat context to the cache.

        Args:
            context (ChatContext): The ChatContext object to cache.
        key = f"chat_context:{context.agent_id}"
        # The ChatContext object would need a serializable representation.
        # Pydantic's model_dump_json is a good candidate.
        await self._client.set(key, context.model_dump_json(), ex=3600) # 1 hour TTL

    async def delete_chat_context(self, agent_id: str) -> None:
        Deletes a chat context from the cache.

        Args:
            agent_id (str): The ID of the agent whose context should be deleted.
        await self._client.delete(f"chat_context:{agent_id}")

"""
