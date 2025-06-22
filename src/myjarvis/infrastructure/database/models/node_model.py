"""SQLAlchemy Node model.

This module defines the `NodeModel`, the SQLAlchemy ORM model for the `nodes` table.
It represents a "Node", which is an external service or tool that an AI Agent can use.

Implementation Details:
- The class should inherit from a declarative base.
- It should define columns for the `Node` entity attributes:
  - `id`: Primary key.
  - `node_id`: A unique identifier for the node (Value Object).
  - `name`: The name of the node (e.g., "Google Docs", "Email Sender").
  - `description`: A text description of what the node does, for the LLM to understand.
  - `node_type`: A string identifying the type of node (e.g., 'google_docs', 'search').
- It should define the many-to-many relationship with `AgentModel` if not already defined
  on the agent side, but typically this is managed via the `agent_model`'s relationship
  and a separate association table.
"""
