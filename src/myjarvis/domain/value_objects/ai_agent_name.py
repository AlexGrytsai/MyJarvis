from dataclasses import dataclass

from src.myjarvis.domain.exceptions import UnavailableAgentName


@dataclass(frozen=True, slots=True)
class AgentName:
    value: str

    def __post_init__(self) -> None:
        if not self.value:
            raise UnavailableAgentName("Agent name cannot be empty")
        if len(self.value) > 100:
            raise UnavailableAgentName(
                "Agent name cannot be longer than 100 characters"
            )

    def __str__(self) -> str:
        return self.value
