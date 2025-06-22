"""
This module will contain the Pydantic schemas for AI agent-related data.

These schemas will be used for:
- Validating the data received in API requests for creating and updating agents.
- Serializing the agent data sent in API responses.
- Generating OpenAPI documentation for the agent endpoints.

Implementation Details:
- Create a base schema `AgentBase` with common fields.
- Create an `AgentCreate` schema for creating new agents, inheriting from
  `AgentBase`. It will include fields like `name`, `base_prompt`, and
  `llm_model`.
- Create an `AgentUpdate` schema for updating existing agents, inheriting from
  `AgentBase`. All fields should be optional.
- Create an `AgentRead` schema for representing agents in API responses,
  inheriting from `AgentBase`. It will include read-only fields like `id`,
  `user_id`, and `created_at`, as well as a list of attached nodes.

Example:
    from pydantic import BaseModel, Field
    from uuid import UUID
    from datetime import datetime

    class AgentBase(BaseModel):
        name: str = Field(..., min_length=1, max_length=100)
        base_prompt: str | None = None
        llm_model: str = "gpt-4"

    class AgentCreate(AgentBase):
        pass

    class AgentUpdate(BaseModel):
        name: str | None = Field(None, min_length=1, max_length=100)
        base_prompt: str | None = None
        llm_model: str | None = None

    class AgentRead(AgentBase):
        id: UUID
        user_id: UUID
        created_at: datetime
        # attached_nodes: list[NodeRead] # Assuming NodeRead is defined

        class Config:
            from_attributes = True
"""
