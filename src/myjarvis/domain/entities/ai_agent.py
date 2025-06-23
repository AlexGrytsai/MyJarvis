"""
This module defines the AIAgent entity.

The AIAgent is a core entity of the domain. It represents an AI agent that can
be created by a User. Each agent has a specific configuration, including a base
prompt, a selected LLM model, and a set of connected Nodes (tools) that it can
use.

Implementation details:
- The class should be a Pydantic BaseModel for data validation.
- It should include fields like `agent_id`, `user_id`, `name`, `base_prompt`,
  `llm_model`, `created_at`, and a list of `node_ids`.
- It should contain business logic methods such as `attach_node`,
  `detach_node`, `update_prompt`, etc.
- The entity should ensure its invariants, for example, an agent cannot have
  duplicate nodes.
"""

from datetime import datetime, timezone
from typing import List

from pydantic import BaseModel, Field

from myjarvis.domain.value_objects import AgentId, NodeId, UserId


class AIAgent(BaseModel):
    """
    The AIAgent is a core entity of the domain. It represents an AI agent that can
    be created by a User. Each agent has a specific configuration, including a base
    prompt, a selected LLM model, and a set of connected Nodes (tools) that it can
    use.
    """
    id: AgentId = Field(default_factory=AgentId)
    user_id: UserId
    name: str
    base_prompt: str
    llm_model: str
    node_ids: List[NodeId] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Config:
        arbitrary_types_allowed = True

    # Business logic methods like attach_node, detach_node, etc.
    # would be added here in the future.
