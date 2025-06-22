"""Command Handlers.

This module contains the handler classes responsible for executing commands. Each handler
is specific to one command and contains the logic to orchestrate the necessary steps
to fulfill that command's purpose.

Implementation Details:
-----------------------
A command bus (or a simple dependency injection mechanism) will be used to map a
command to its corresponding handler. Each handler will be a class with a `handle`
or `__call__` method that accepts a command object.

Handlers to be implemented here include:

- `CreateAgentHandler`:
  - Receives `CreateAgentCommand`.
  - Creates a new `AIAgent` entity instance.
  - Uses `UserRepository` to verify the user exists.
  - Uses `AgentRepository` to persist the new agent.

- `AttachNodeHandler`:
  - Receives `AttachNodeCommand`.
  - Uses `AgentRepository` to find the agent.
  - Uses `NodeRepository` to find the node.
  - Validates that the user in the command owns the agent.
  - Invokes a domain service or an agent method (e.g., `agent.attach_node(node)`).
  - Uses `AgentRepository` to save the updated agent state.

- `SendMessageHandler`:
  - Receives `SendMessageCommand`.
  - This is the most complex handler. It will retrieve the agent, nodes, and chat
    context using repositories.
  - It will then call a `ChatService` or `AgentService` in the domain layer,
    passing the necessary information.
  - The domain service will be responsible for the core logic of interacting with
    the LLM and processing the response.
  - The handler will persist the updated chat context.
"""
