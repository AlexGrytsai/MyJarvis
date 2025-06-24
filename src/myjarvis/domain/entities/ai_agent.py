from __future__ import annotations

from dataclasses import dataclass, field, InitVar
from datetime import datetime, timezone
from typing import Callable, List, Optional

from src.myjarvis.domain.value_objects import (
    AgentId,
    NodeId,
    UserId,
)
from src.myjarvis.domain.value_objects.ai_agent_name import AgentName
from src.myjarvis.domain.value_objects.llm_model import LlmModel


@dataclass
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
        self._clock = clock or (lambda: datetime.now(timezone.utc))

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

    def delete(self) -> bool:
        """Mark the agent as deleted (soft delete)."""
        if not self.is_deleted:
            self.deleted_at = self._clock()
            self._touch()
            return True
        return False

    def restore(self) -> bool:
        """Restore a soft-deleted agent."""
        if self.is_deleted:
            self.deleted_at = None
            self._touch()
            return True
        return False

    def update_name(self, new_name: AgentName) -> AIAgent:
        """Update the agent's name."""
        self.name = new_name
        self._touch()

        return self

    def update_description(self, new_description: Optional[str]) -> AIAgent:
        """Update the agent's description."""
        self.description = new_description
        self._touch()

        return self

    def update_prompt(self, new_prompt: Optional[str]) -> AIAgent:
        """Update the agent's base prompt."""
        self.base_prompt = new_prompt
        self._touch()

        return self

    def update_llm_model(self, new_model: LlmModel) -> AIAgent:
        """Update the agent's LLM configuration."""
        self.llm_model = new_model
        self._touch()

        return self

    def attach_node(self, node_id: NodeId) -> bool:
        """
        Attach a node (tool) to the agent.

        Ensures that the same node is not attached more than once.
        """
        if node_id not in self.node_ids:
            self.node_ids.append(node_id)
            self._touch()
            return True
        return False

    def detach_node(self, node_id: NodeId) -> bool:
        """
        Detach a node (tool) from the agent.

        Handles cases where the node is not attached.
        """
        if node_id in self.node_ids:
            self.node_ids.remove(node_id)
            self._touch()
            return True
        return False

    def _touch(self) -> None:
        """Update the timestamp to the current time using the entity's clock."""
        self.updated_at = self._clock()
