"""
This module defines the base interface for all Large Language Model (LLM) providers.

It contains an abstract base class `BaseLlm` that all specific LLM implementations
(e.g., OpenAI, Anthropic, Gemini) must inherit from. This ensures that the application
can interact with different LLM providers through a consistent interface.

The `BaseLlm` class should define a standard method for generating responses,
handling chat history, and managing model-specific configurations.

Example Implementation:

from abc import ABC, abstractmethod
from myjarvis.domain.value_objects.message import Message

class BaseLlm(ABC):
    @abstractmethod
    async def generate_response(
        self,
        prompt: str,
        history: list[Message] | None = None,
        **kwargs
    ) -> str:
        Generates a response from the LLM based on a given prompt and chat history.

        Args:
            prompt (str): The user's input prompt.
            history (list[Message] | None): A list of previous messages in the chat
                                            to provide context. Defaults to None.
            **kwargs: Additional model-specific parameters.

        Returns:
            str: The generated text response from the LLM.
        pass
"""
