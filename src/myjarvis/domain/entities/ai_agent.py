from __future__ import annotations

import logging
from dataclasses import dataclass, field, InitVar
from datetime import datetime, timezone
from typing import Callable, List, Optional

from src.myjarvis.domain.repositories import NodeRepository
from src.myjarvis.domain.value_objects import (
    AgentId,
    NodeId,
    UserId,
)
from src.myjarvis.domain.value_objects.ai_agent_name import AgentName
from src.myjarvis.domain.value_objects.llm_model import LlmModel

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class AIAgent:
    """
    The AIAgent is a core domain entity.
    It represents an AI agent created by a User.

    Each agent has a specific configuration, including a base prompt,
    a selected LLM model, and a set of connected Nodes (tools) that it can use.
    This class encapsulates the state and business logic of the agent.
    """

    id: AgentId
    user_id: UserId
    name: AgentName
    llm_model: LlmModel

    created_at: datetime
    updated_at: datetime

    description: Optional[str] = None
    base_prompt: Optional[str] = None
    node_ids: List[NodeId] = field(default_factory=list)

    deleted_at: Optional[datetime] = field(default=None)

    clock: InitVar[Optional[Callable[[], datetime]]] = None
    _clock: Callable[[], datetime] = field(init=False, repr=False)

    def __post_init__(self, clock: Optional[Callable[[], datetime]]):
        object.__setattr__(
            self, "_clock", clock or (lambda: datetime.now(timezone.utc))
        )

    @classmethod
    def create(
        cls,
        agent_id: AgentId,
        user_id: UserId,
        name: AgentName,
        llm_model: LlmModel,
        clock: Optional[Callable[[], datetime]] = None,
    ) -> AIAgent:
        """Factory method to create a new agent."""
        _clock = clock or (lambda: datetime.now(timezone.utc))
        now = _clock()
        return cls(
            id=agent_id,
            user_id=user_id,
            name=name,
            llm_model=llm_model,
            created_at=now,
            updated_at=now,
            clock=clock,
        )

    @property
    def is_deleted(self) -> bool:
        """Check if the agent is marked as deleted."""
        return self.deleted_at is not None

    def delete(self) -> AIAgent:
        """Mark the agent as deleted (soft delete)."""
        if not self.is_deleted:
            return AIAgent(
                id=self.id,
                user_id=self.user_id,
                name=self.name,
                llm_model=self.llm_model,
                created_at=self.created_at,
                updated_at=self._clock(),
                description=self.description,
                base_prompt=self.base_prompt,
                node_ids=self.node_ids.copy(),
                deleted_at=self._clock(),
                clock=self._clock,
            )
        return self

    def restore(self) -> AIAgent:
        """Restore a soft-deleted agent."""
        if self.is_deleted:
            return AIAgent(
                id=self.id,
                user_id=self.user_id,
                name=self.name,
                llm_model=self.llm_model,
                created_at=self.created_at,
                updated_at=self._clock(),
                description=self.description,
                base_prompt=self.base_prompt,
                node_ids=self.node_ids.copy(),
                deleted_at=None,
                clock=self._clock,
            )
        return self

    def update_name(self, new_name: AgentName) -> AIAgent:
        """Update the agent's name."""
        return AIAgent(
            id=self.id,
            user_id=self.user_id,
            name=new_name,
            llm_model=self.llm_model,
            created_at=self.created_at,
            updated_at=self._clock(),
            description=self.description,
            base_prompt=self.base_prompt,
            node_ids=self.node_ids.copy(),
            deleted_at=self.deleted_at,
            clock=self._clock,
        )

    def update_description(self, new_description: Optional[str]) -> AIAgent:
        """Update the agent's description."""
        return AIAgent(
            id=self.id,
            user_id=self.user_id,
            name=self.name,
            llm_model=self.llm_model,
            created_at=self.created_at,
            updated_at=self._clock(),
            description=new_description,
            base_prompt=self.base_prompt,
            node_ids=self.node_ids.copy(),
            deleted_at=self.deleted_at,
            clock=self._clock,
        )

    def update_prompt(self, new_prompt: Optional[str]) -> AIAgent:
        """Update the agent's base prompt."""
        return AIAgent(
            id=self.id,
            user_id=self.user_id,
            name=self.name,
            llm_model=self.llm_model,
            created_at=self.created_at,
            updated_at=self._clock(),
            description=self.description,
            base_prompt=new_prompt,
            node_ids=self.node_ids.copy(),
            deleted_at=self.deleted_at,
            clock=self._clock,
        )

    def update_llm_model(self, new_model: LlmModel) -> AIAgent:
        """Update the agent's LLM configuration."""
        return AIAgent(
            id=self.id,
            user_id=self.user_id,
            name=self.name,
            llm_model=new_model,
            created_at=self.created_at,
            updated_at=self._clock(),
            description=self.description,
            base_prompt=self.base_prompt,
            node_ids=self.node_ids.copy(),
            deleted_at=self.deleted_at,
            clock=self._clock,
        )

    def attach_node(
        self,
        node_id: NodeId,
        node_repository: NodeRepository,
    ) -> AIAgent:
        node = node_repository.get_by_id(node_id)
        if (
            node is None
            or getattr(node, "deleted", False)
            or getattr(node, "deactivated", False)
        ):
            return self
        if node_id not in self.node_ids:
            new_node_ids = self.node_ids.copy()
            new_node_ids.append(node_id)
            return AIAgent(
                id=self.id,
                user_id=self.user_id,
                name=self.name,
                llm_model=self.llm_model,
                created_at=self.created_at,
                updated_at=self._clock(),
                description=self.description,
                base_prompt=self.base_prompt,
                node_ids=new_node_ids,
                deleted_at=self.deleted_at,
                clock=self._clock,
            )
        return self

    def detach_node(self, node_id: NodeId) -> AIAgent:
        """
        Detach a node (tool) from the agent.

        Handles cases where the node is not attached.
        """
        if node_id in self.node_ids:
            new_node_ids = self.node_ids.copy()
            new_node_ids.remove(node_id)
            return AIAgent(
                id=self.id,
                user_id=self.user_id,
                name=self.name,
                llm_model=self.llm_model,
                created_at=self.created_at,
                updated_at=self._clock(),
                description=self.description,
                base_prompt=self.base_prompt,
                node_ids=new_node_ids,
                deleted_at=self.deleted_at,
                clock=self._clock,
            )
        logger.warning(
            f"Attempted to detach node_id {node_id} which was not attached."
        )
        return self
