from dataclasses import dataclass
from typing import Optional

from src.myjarvis.domain.exceptions import (
    TemperatureNotValid,
    MaxTokensNotValid,
)
from src.myjarvis.domain.value_objects.llm_provider import LlmProvider


@dataclass(frozen=True)
class LlmModel:
    provider: LlmProvider
    model_name: str
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

    def __post_init__(self):
        if self.temperature is not None and not (0 <= self.temperature <= 1):
            raise TemperatureNotValid("Temperature must be between 0 and 1")

        if self.max_tokens is not None and self.max_tokens <= 0:
            raise MaxTokensNotValid("Max tokens must be greater than 0")

    def __str__(self):
        return f"{self.provider.value}:{self.model_name}"
