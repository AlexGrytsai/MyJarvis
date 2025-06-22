"""Get User Agents Query.

This module defines the query for retrieving a list of all AI agents belonging to a
specific user. This query is part of the Application layer and follows the CQRS pattern.

Implementation Details:
-----------------------
This file should contain a Pydantic model or a dataclass named `GetUserAgentsQuery`
that encapsulates the parameters needed to fetch the agents.

`GetUserAgentsQuery` should include:
- `user_id`: The unique identifier for the user whose agents are to be retrieved.

The handler for this query, `GetUserAgentsHandler`, will be located in the
`application.handlers.query_handlers` module. It will receive this query object,
use a read-only repository to fetch the data, and return a list of `AgentDTO`
objects (`list[AgentDTO]`). The data returned should be concise, perhaps omitting
details like the full base prompt, suitable for a list view.
"""
