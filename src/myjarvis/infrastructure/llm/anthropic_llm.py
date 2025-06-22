"""
This module provides the implementation for interacting with Anthropic's LLMs.

It contains the `AnthropicLlm` class that inherits from `BaseLlm` and implements
the methods for generating responses using the Anthropic API (e.g., Claude models).
This class will manage the API key, model selection, and the specifics of
communicating with the Anthropic API.

Example Implementation:

import os
from anthropic import AsyncAnthropic
from myjarvis.domain.value_objects.message import Message
from myjarvis.infrastructure.llm.base_llm import BaseLlm

class AnthropicLlm(BaseLlm):
    def __init__(self, api_key: str | None = None, model: str = "claude-3-opus-20240229"):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key is not provided.")
        self.client = AsyncAnthropic(api_key=self.api_key)
        self.model = model

    async def generate_response(
        self,
        prompt: str,
        history: list[Message] | None = None,
        **kwargs
    ) -> str:
        # Implementation to call the Anthropic API.
        # It should handle the conversion of the chat history and prompt
        # to the format expected by the Anthropic client.
        pass
"""
