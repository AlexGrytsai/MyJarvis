"""Node Data Transfer Object.

This module defines the Data Transfer Object (DTO) for a Node.
Nodes represent the tools and services that can be attached to an AI agent.

Implementation Details:
-----------------------
This file should contain a Pydantic model named `NodeDTO`. It provides a public
representation of a `Node` entity.

The `NodeDTO` should include fields such as:
- `id`: The unique identifier of the node.
- `name`: The human-readable name of the node (e.g., "Google Calendar").
- `description`: A text explaining what the node does, which can be used by the
  LLM to understand its capabilities.
- `available_commands`: A list of commands the node can execute.

This DTO will be used within `AgentDTO` to show which nodes are attached, and it
can also be returned by queries that list all available nodes in the system.
"""
