"""
Agent Data Transfer Object.

This module defines the Data Transfer Object (DTO) for an AI agent.
DTOs are used to transfer data between the application layer and the
presentation layer, providing a decoupled and serializable representation of
domain entities.

Implementation Details:
-----------------------
This file should contain a Pydantic model named `AgentDTO`. It should represent
the state of an `AIAgent` entity that is safe to expose to external clients (like a
web frontend or an API consumer).

The `AgentDTO` should include fields such as:
- `id`: The unique identifier of the agent.
- `name`: The name of the agent.
- `base_prompt`: The system prompt of the agent.
- `llm_model`: The identifier of the language model used.
- `created_at`: The timestamp of when the agent was created.
- `attached_nodes`: A list of `NodeDTO` objects representing the tools
  connected to this agent.

This DTO will be constructed by query handlers in the `application.handlers.query_handlers`
module and returned to the presentation layer.
"""
