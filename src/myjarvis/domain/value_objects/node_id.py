from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class NodeId:
    """
    NodeId is a unique identifier for a Node entity.

    Using a dedicated type for the ID improves type safety and makes the
    domain model more explicit.
    """

    value: UUID

    def __str__(self) -> str:
        return str(self.value)
