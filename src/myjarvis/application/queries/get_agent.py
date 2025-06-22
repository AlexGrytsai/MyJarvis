"""Get Agent Query.

This module defines the query for retrieving detailed information about a single AI agent.
This query is part of the Application layer and follows the CQRS pattern.

Implementation Details:
-----------------------
This file should contain a Pydantic model or a dataclass named `GetAgentQuery`
that encapsulates the parameters needed to fetch an agent.

`GetAgentQuery` should include:
- `agent_id`: The unique identifier for the agent to be retrieved.
- `user_id`: The ID of the user requesting the information, to ensure they have
  permission to view the agent.

The handler for this query, `GetAgentHandler`, will be located in the
`application.handlers.query_handlers` module. It will receive this query object,
use a read-only repository or query service to fetch the data, and return an
`AgentDTO` object from the `application.dto` package. The handler must verify that
the `user_id` matches the one associated with the agent.
"""
