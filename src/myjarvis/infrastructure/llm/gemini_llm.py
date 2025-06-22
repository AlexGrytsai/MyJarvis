"""
This module provides the implementation for interacting with Google's Gemini LLMs.

It contains the `GeminiLlm` class that inherits from `BaseLlm`. This class is
responsible for connecting to the Google AI Platform and using the Gemini models
to generate text responses. It will handle authentication (e.g., API key),
model selection (e.g., "gemini-pro"), and the request/response lifecycle for the
Google Generative AI API.

Example Implementation:

import os
import google.generativeai as genai
from myjarvis.domain.value_objects.message import Message
from myjarvis.infrastructure.llm.base_llm import BaseLlm

class GeminiLlm(BaseLlm):
    def __init__(self, api_key: str | None = None, model: str = "gemini-pro"):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key is not provided.")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)

    async def generate_response(
        self,
        prompt: str,
        history: list[Message] | None = None,
        **kwargs
    ) -> str:
        # Implementation to call the Google Gemini API.
        # It might need to start a chat session from the history
        # and then send the new prompt.
        pass
"""
