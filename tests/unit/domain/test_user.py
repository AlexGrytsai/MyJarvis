import uuid
from datetime import datetime

import pytest

from src.myjarvis.domain.entities.user import User
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


@pytest.fixture
def user_id() -> UserId:
    return UserId(uuid.uuid4())


@pytest.fixture
def email() -> Email:
    return Email("test@example.com")


@pytest.fixture
def username() -> str:
    return "testuser"


@pytest.fixture
def user(user_id: UserId, email: Email, username: str) -> User:
    return User.create(user_id=user_id, email=email, username=username)


class TestUser:
    def test_create_user(self, user_id: UserId, email: Email, username: str):
        user = User.create(user_id=user_id, email=email, username=username)

        assert user.id == user_id
        assert user.email == email
        assert user.username == username
        assert user.telegram_id is None
        assert user.llm_api_keys == {}
        assert user.agent_ids == set()
        assert isinstance(user.created_at, datetime)
        assert isinstance(user.updated_at, datetime)

    def test_create_user_without_username(self, user_id: UserId, email: Email):
        user = User.create(user_id=user_id, email=email)
        assert user.username is None

    def test_change_email_successfully(self, user: User):
        new_email = Email("new.email@example.com")
        original_updated_at = user.updated_at

        user.change_email(new_email)

        assert user.email == new_email
        assert user.updated_at > original_updated_at

    def test_change_email_to_same_email_raises_exception(self, user: User):
        with pytest.raises(NewEmailSameAsCurrent):
            user.change_email(user.email)

    def test_change_email_to_same_email_different_case_raises_exception(
        self, user: User
    ):
        same_email_different_case = Email(str(user.email).upper())
        with pytest.raises(NewEmailSameAsCurrent):
            user.change_email(same_email_different_case)

    def test_change_username_successfully(self, user: User):
        new_username = "new_username"
        original_updated_at = user.updated_at

        user.change_username(new_username)

        assert user.username == new_username
        assert user.updated_at > original_updated_at

    def test_change_username_to_none_successfully(self, user: User):
        user.change_username(None)
        assert user.username is None

    def test_change_username_to_empty_string(self, user: User):
        user.change_username("")
        assert user.username == ""

    def test_change_username_to_same_username_raises_exception(
        self, user: User
    ):
        with pytest.raises(NewUsernameSameAsCurrent):
            user.change_username(user.username)

    def test_add_api_key_successfully(self, user: User):
        api_key = LlmApiKey(provider=LlmProvider.OPENAI, key="test_key")
        original_updated_at = user.updated_at

        user.add_api_key(api_key)

        assert LlmProvider.OPENAI in user.llm_api_keys
        assert user.llm_api_keys[LlmProvider.OPENAI] == api_key
        assert user.updated_at > original_updated_at

    def test_add_existing_api_key_raises(self, user: User):
        api_key = LlmApiKey(provider=LlmProvider.OPENAI, key="test_key")
        user.add_api_key(api_key)

        with pytest.raises(LLMProviderAlreadyExistsInUser):
            user.add_api_key(api_key)

    def test_update_llm_api_key_successfully(self, user: User):
        provider = LlmProvider.GEMINI
        initial_api_key = LlmApiKey(provider=provider, key="initial_key")
        user.add_api_key(initial_api_key)

        updated_api_key = LlmApiKey(provider=provider, key="updated_key")
        original_updated_at = user.updated_at

        user.update_llm_api_key(updated_api_key)

        assert user.llm_api_keys[provider] == updated_api_key
        assert user.updated_at > original_updated_at

    def test_update_non_existent_api_key_raises(self, user: User):
        api_key = LlmApiKey(provider=LlmProvider.ANTHROPIC, key="test_key")
        with pytest.raises(LLMProviderNotExistsInUser):
            user.update_llm_api_key(api_key)

    def test_remove_llm_api_key_successfully(self, user: User):
        provider = LlmProvider.OPENAI
        api_key = LlmApiKey(provider=provider, key="test_key")
        user.add_api_key(api_key)
        original_updated_at = user.updated_at

        user.remove_llm_api_key(provider)

        assert provider not in user.llm_api_keys
        assert user.updated_at > original_updated_at

    def test_remove_non_existent_api_key_raises(self, user: User):
        with pytest.raises(LLMProviderNotExistsInUser):
            user.remove_llm_api_key(LlmProvider.OPENAI)

    def test_add_agent_successfully(self, user: User):
        agent_id = AgentId(uuid.uuid4())
        original_updated_at = user.updated_at

        user.add_agent(agent_id)

        assert agent_id in user.agent_ids
        assert user.updated_at > original_updated_at

    def test_add_multiple_agents_successfully(self, user: User):
        agent_id1 = AgentId(uuid.uuid4())
        agent_id2 = AgentId(uuid.uuid4())

        user.add_agent(agent_id1)
        user.add_agent(agent_id2)

        assert agent_id1 in user.agent_ids
        assert agent_id2 in user.agent_ids
        assert len(user.agent_ids) == 2

    def test_add_existing_agent_does_not_change_state(self, user: User):
        agent_id = AgentId(uuid.uuid4())
        user.add_agent(agent_id)
        original_agent_ids = user.agent_ids.copy()
        original_updated_at = user.updated_at

        user.add_agent(agent_id)

        assert user.agent_ids == original_agent_ids
        assert user.updated_at == original_updated_at

    def test_remove_agent_successfully(self, user: User):
        agent_id = AgentId(uuid.uuid4())
        user.add_agent(agent_id)
        original_updated_at = user.updated_at

        user.remove_agent(agent_id)

        assert agent_id not in user.agent_ids
        assert user.updated_at > original_updated_at

    def test_remove_non_existent_agent_raises_exception(self, user: User):
        agent_id = AgentId(uuid.uuid4())
        with pytest.raises(AgentNotFoundInUser):
            user.remove_agent(agent_id)

    def test_touch_updates_timestamp(self, user: User):
        original_updated_at = user.updated_at
        user._touch()
        assert user.updated_at > original_updated_at
