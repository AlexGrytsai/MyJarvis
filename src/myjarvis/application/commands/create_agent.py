"""Create Agent Command.

This module defines the command for creating a new AI agent. This command is part of the
Application layer and follows the CQRS pattern.

Implementation Details:
-----------------------
This file should contain a Pydantic model or a dataclass named `CreateAgentCommand`
that encapsulates the data required to create a new agent.

`CreateAgentCommand` should include:
- `user_id`: The ID of the user creating the agent.
- `name`: The name of the new agent.
- `base_prompt`: The initial system prompt for the agent.
- `llm_model`: The identifier for the Language Model to be used (e.g., 'openai-gpt-4').

The handler for this command, `CreateAgentHandler`, will be located in the
`application.handlers.command_handlers` module. It will receive this command object,
create an `AIAgent` entity, and save it using the `AgentRepository`.
"""
