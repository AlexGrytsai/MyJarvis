from dataclasses import dataclass

from src.myjarvis.domain.value_objects import LlmProvider


@dataclass(frozen=True)
class LlmApiKey:
    """
    Represents an encrypted API key for a specific Large Language Model (LLM)
    provider.

    Attributes:
        provider (LlmProvider): The provider of the LLM,
                                e.g. OpenAI, Anthropic, Gemini.
        encrypted_key (str): The encrypted API key for the LLM provider.
    """

    provider: LlmProvider
    encrypted_key: str

    def __str__(self) -> str:
        return self.encrypted_key
