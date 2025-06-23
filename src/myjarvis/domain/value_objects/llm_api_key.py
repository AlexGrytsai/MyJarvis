from dataclasses import dataclass

from src.myjarvis.domain.value_objects.llm_provider import LlmProvider


@dataclass(frozen=True)
class LlmApiKey:
    """
    Represents an API key for a specific Large Language Model (LLM)
    provider.

    Attributes:
        provider (LlmProvider): The provider of the LLM,
                                e.g. OpenAI, Anthropic, Gemini.
        key (str): The API key for the LLM provider.
    """

    provider: LlmProvider
    key: str

    def __str__(self) -> str:
        return f"***{self.key[-4:]}" if len(self.key) > 4 else "***"
