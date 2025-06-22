"""Query Handlers.

This module contains the handler classes responsible for executing queries. Each handler
is specific to one query. Query handlers are responsible for fetching data from a
persistence mechanism (via repositories) and mapping it to Data Transfer Objects (DTOs).

Query handlers should not have any side effects and must not modify system state.

Implementation Details:
-----------------------
Similar to command handlers, a query bus or dependency injection will map queries to
their respective handlers.

Handlers to be implemented here include:

- `GetAgentHandler`:
  - Receives `GetAgentQuery`.
  - Uses a read-only method on `AgentRepository` to fetch the agent data by its ID.
  - Verifies that the `user_id` from the query matches the agent's owner.
  - Maps the retrieved data to an `AgentDTO`.
  - Returns the `AgentDTO`.

- `GetUserAgentsHandler`:
  - Receives `GetUserAgentsQuery`.
  - Uses a read-only method on `AgentRepository` to fetch all agents for a given
    `user_id`.
  - Maps the list of retrieved data to a list of `AgentDTO` objects (`list[AgentDTO]`).
  - Returns the list of DTOs.
"""
