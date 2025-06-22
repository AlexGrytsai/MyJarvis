from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(frozen=True, slots=True)
class AgentId:
    """
    Unique identifier for an AI Agent entity.

    This value object wraps a UUID and provides a string representation.
    """

    value: UUID = field(default_factory=uuid4)

    def __str__(self) -> str:
        return str(self.value)
