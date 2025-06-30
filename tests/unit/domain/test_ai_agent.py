from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.myjarvis.domain.entities import AIAgent
from src.myjarvis.domain.value_objects import UserId, AgentId, NodeId
from src.myjarvis.domain.value_objects.ai_agent_name import (
    AgentName,
    UnavailableAgentName,
)
from src.myjarvis.domain.value_objects.llm_model import (
    LlmModel,
    TemperatureNotValid,
    MaxTokensNotValid,
)
from src.myjarvis.domain.value_objects.llm_provider import LlmProvider


def make_agent(clock=None):
    return AIAgent.create(
        agent_id=AgentId(uuid4()),
        user_id=UserId(uuid4()),
        name=AgentName("TestAgent"),
        llm_model=LlmModel(LlmProvider.OPENAI, "gpt-3.5"),
        clock=clock,
    )


def test_create_agent_sets_fields():
    agent = make_agent()
    assert isinstance(agent.id, AgentId)
    assert isinstance(agent.user_id, UserId)
    assert isinstance(agent.name, AgentName)
    assert isinstance(agent.llm_model, LlmModel)
    assert agent.created_at == agent.updated_at
    assert agent.deleted_at is None
    assert agent.node_ids == []
    assert not agent.is_deleted


def test_delete_and_restore():
    agent = make_agent()
    assert agent.delete() is True
    assert agent.is_deleted
    deleted_at = agent.deleted_at
    assert deleted_at is not None
    assert agent.delete() is False
    assert agent.deleted_at == deleted_at
    assert agent.restore() is True
    assert not agent.is_deleted
    assert agent.deleted_at is None
    assert agent.restore() is False


def test_update_name():
    agent = make_agent()
    old_updated = agent.updated_at
    agent.update_name(AgentName("NewName"))
    assert agent.name.value == "NewName"
    assert agent.updated_at > old_updated


def test_update_description():
    agent = make_agent()
    agent.update_description("desc")
    assert agent.description == "desc"
    agent.update_description(None)
    assert agent.description is None


def test_update_prompt():
    agent = make_agent()
    agent.update_prompt("prompt")
    assert agent.base_prompt == "prompt"
    agent.update_prompt(None)
    assert agent.base_prompt is None


def test_update_llm_model():
    agent = make_agent()
    new_model = LlmModel(
        LlmProvider.ANTHROPIC, "claude", temperature=0.5, max_tokens=100
    )
    agent.update_llm_model(new_model)
    assert agent.llm_model == new_model


def test_attach_and_detach_node():
    agent = make_agent()
    node1 = NodeId(uuid4())
    node2 = NodeId(uuid4())
    assert agent.attach_node(node1) is True
    assert node1 in agent.node_ids
    assert agent.attach_node(node1) is False
    assert agent.attach_node(node2) is True
    assert node2 in agent.node_ids
    assert agent.detach_node(node1) is True
    assert node1 not in agent.node_ids
    assert agent.detach_node(node1) is False
    assert agent.detach_node(node2) is True
    assert agent.node_ids == []


def test_touch_updates_updated_at():
    times = [
        datetime(2023, 1, 1, tzinfo=timezone.utc),
        datetime(2023, 1, 2, tzinfo=timezone.utc),
    ]

    def clock():
        return times.pop(0)

    agent = make_agent(clock=clock)
    old_updated = agent.updated_at
    agent.update_name(AgentName("X"))
    assert agent.updated_at > old_updated


def test_agent_name_constraints():
    with pytest.raises(UnavailableAgentName):
        AgentName("")
    with pytest.raises(UnavailableAgentName):
        AgentName("a" * 101)


def test_llm_model_constraints():
    with pytest.raises(TemperatureNotValid):
        LlmModel(LlmProvider.OPENAI, "gpt", temperature=-1)
    with pytest.raises(TemperatureNotValid):
        LlmModel(LlmProvider.OPENAI, "gpt", temperature=2)
    with pytest.raises(MaxTokensNotValid):
        LlmModel(LlmProvider.OPENAI, "gpt", max_tokens=0)
