"""SQLAlchemy AI Agent model.

This module defines the `AgentModel` class, the SQLAlchemy ORM model for the `agents` table.
It represents the persistent state of an `AIAgent` domain entity.

Implementation Details:
- The class should inherit from a declarative base.
- It must define columns for the `AIAgent` attributes:
  - `id`: Primary key.
  - `agent_id`: A unique identifier for the agent (Value Object).
  - `user_id`: A foreign key to the `users` table, linking the agent to its owner.
  - `name`: The name of the agent.
  - `base_prompt`: The initial prompt or instruction for the agent.
  - `llm_model`: A string indicating the LLM model used (e.g., 'openai', 'anthropic').
  - `created_at`: Timestamp of agent creation.
- It should define the many-to-one relationship back to the `UserModel`:
  - `user = relationship("UserModel", back_populates="agents")`
- It should also define a many-to-many relationship with `NodeModel` to represent
  the nodes attached to this agent. This will require an association table.
  - `nodes = relationship("NodeModel", secondary="agent_nodes_association")`
"""
