"""
This module defines the repository interface for the Node entity.

This interface provides a contract for persistence operations related to nodes,
abstracting the underlying data storage mechanism.

Implementation details:
- The interface should be an abstract base class (ABC).
- It should define asynchronous methods for managing nodes, such as:
  - `add(node: Node) -> None`
  - `get_by_id(node_id: NodeId) -> Node | None`
  - `list_all() -> list[Node]`
  - `update(node: Node) -> None`
  - `delete(node_id: NodeId) -> None`
- Implementations of this interface will reside in the infrastructure layer.
"""

from abc import ABC, abstractmethod
from typing import Optional

from src.myjarvis.domain.entities import Node


class NodeRepository(ABC):

    @abstractmethod
    def get_by_id(self, node_id: str) -> Optional[Node]:
        """Retrieves a Node by its unique ID."""
        pass
