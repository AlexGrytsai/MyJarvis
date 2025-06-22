"""
This module defines the repository interface for the AIAgent entity.

This interface provides a contract for persistence operations related to AI
agents, abstracting the underlying data storage mechanism.

Implementation details:
- The interface should be an abstract base class (ABC).
- It should define asynchronous methods for CRUD operations, such as:
  - `add(agent: AIAgent) -> None`
  - `get_by_id(agent_id: AgentId) -> AIAgent | None`
  - `get_all_by_user_id(user_id: UserId) -> list[AIAgent]`
  - `update(agent: AIAgent) -> None`
  - `delete(agent_id: AgentId) -> None`
- Implementations of this interface will reside in the infrastructure layer.
"""
