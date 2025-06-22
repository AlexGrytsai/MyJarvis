"""SQLAlchemy implementation of the AgentRepository.

This module contains the `SQLAlchemyAgentRepository`, which is the concrete
implementation of the `AgentRepository` interface from the domain layer.
It handles the persistence of `AIAgent` entities using SQLAlchemy.

Implementation Details:
- The class `SQLAlchemyAgentRepository` should inherit from `AgentRepository`.
- It depends on an `AsyncSession` for all database operations.
- It must implement methods like:
  - `add(agent: AIAgent)`: Persists a new `AIAgent` entity.
  - `get_by_id(agent_id: AgentID)`: Fetches an agent by its ID. It should eagerly
    load related nodes to avoid lazy loading issues.
  - `list_by_user_id(user_id: UserID)`: Retrieves all agents for a given user.
  - `update(agent: AIAgent)`: Updates an existing agent, including its attached nodes.
- Mapping between the `AIAgent` domain entity and the `AgentModel` ORM model
  is a key responsibility. This includes handling the many-to-many relationship
  with nodes. Helper methods for mapping are recommended.
""" 