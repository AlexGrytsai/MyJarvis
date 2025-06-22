"""
This module provides the implementation for interacting with OpenAI's LLMs.

It contains the `OpenAiLlm` class that inherits from `BaseLlm` and implements
the necessary methods to generate responses using the OpenAI API. This class
will handle API key management, model selection (e.g., "gpt-4", "gpt-3.5-turbo"),
and formatting requests and responses according to the OpenAI API specifications.

Example Implementation:

import os
from openai import AsyncOpenAI
from myjarvis.domain.value_objects.message import Message
from myjarvis.infrastructure.llm.base_llm import BaseLlm

class OpenAiLlm(BaseLlm):
    def __init__(self, api_key: str | None = None, model: str = "gpt-4"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is not provided.")
        self.client = AsyncOpenAI(api_key=self.api_key)
        self.model = model

    async def generate_response(
        self,
        prompt: str,
        history: list[Message] | None = None,
        **kwargs
    ) -> str:
        # Implementation to call the OpenAI API
        # It should format the history and prompt into the required
        # message format for the OpenAI client.
        pass
"""
