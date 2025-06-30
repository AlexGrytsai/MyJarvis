from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class AgentId:
    """
    Unique identifier for an AI Agent entity.

    This value object wraps a UUID and provides a string representation.
    """

    value: UUID

    def __str__(self) -> str:
        return str(self.value)
