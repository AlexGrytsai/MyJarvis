from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Optional, Set

from src.myjarvis.domain.exceptions.domain_exceptions import (
    NewEmailSameAsCurrent,
    NewUsernameSameAsCurrent,
    LLMProviderAlreadyExistsInUser,
    LLMProviderNotExistsInUser,
    AgentNotFoundInUser,
)
from src.myjarvis.domain.value_objects import (
    AgentId,
    Email,
    LlmApiKey,
    UserId,
)
from src.myjarvis.domain.value_objects.llm_provider import LlmProvider


@dataclass
class User:
    """
    User entity represents the root aggregate for a user in the system.
    """

    id: UserId
    email: Email
    username: Optional[str] = None
    telegram_id: Optional[str] = None
    llm_api_keys: Dict[LlmProvider, LlmApiKey] = field(default_factory=dict)
    agent_ids: Set[AgentId] = field(default_factory=set)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @classmethod
    def create(
        cls, user_id: UserId, email: Email, username: Optional[str] = None
    ) -> User:
        """Factory method to create a new user."""
        return cls(id=user_id, email=email, username=username)

    def change_email(self, new_email: Email) -> None:
        """Changes the user's email address."""
        if self.email.value.lower() == new_email.value.lower():
            raise NewEmailSameAsCurrent(
                "New email cannot be the same as the current email."
            )
        self.email = new_email
        self._touch()

    def change_username(self, new_username: Optional[str] = None) -> None:
        """Changes the user's display name."""
        if self.username == new_username:
            raise NewUsernameSameAsCurrent(
                "New username cannot be the same as the current username."
            )
        self.username = new_username
        self._touch()

    def add_api_key(self, api_key: LlmApiKey) -> None:
        """Adds a new API key for an LLM provider."""
        if api_key.provider in self.llm_api_keys:
            raise LLMProviderAlreadyExistsInUser(
                f"API key for provider '{api_key.provider.value}' "
                f"already exists."
            )
        self.llm_api_keys[api_key.provider] = api_key
        self._touch()

    def update_llm_api_key(self, api_key: LlmApiKey):
        """Updates an existing LLM API key."""
        if api_key.provider not in self.llm_api_keys:
            raise LLMProviderNotExistsInUser(
                f"API key for provider '{api_key.provider.value}' not found."
            )
        self.llm_api_keys[api_key.provider] = api_key
        self._touch()

    def remove_llm_api_key(self, provider: LlmProvider):
        """Removes an LLM API key by its provider."""
        if provider not in self.llm_api_keys:
            raise LLMProviderNotExistsInUser(
                f"API key for provider '{provider.value}' not found."
            )
        del self.llm_api_keys[provider]
        self._touch()

    def add_agent(self, agent_id: AgentId):
        """Associates a new AI agent with the user."""
        if agent_id not in self.agent_ids:
            self.agent_ids.add(agent_id)
            self._touch()

    def remove_agent(self, agent_id: AgentId):
        """Removes the association with an AI agent."""
        if agent_id not in self.agent_ids:
            raise AgentNotFoundInUser(
                f"Agent with id '{agent_id}' not found for this user."
            )
        self.agent_ids.remove(agent_id)
        self._touch()

    def _touch(self):
        """Updates the `updated_at` timestamp."""
        self.updated_at = datetime.now(timezone.utc)
