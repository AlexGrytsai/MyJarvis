import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from src.myjarvis.domain.entities.chat_context import ChatContext
from src.myjarvis.domain.value_objects.message import Message
from src.myjarvis.domain.value_objects.message_collection import (
    MessageCollection,
)
from src.myjarvis.domain.value_objects.chat_limits import ChatLimits
from src.myjarvis.domain.services.message_operations_service import (
    MessageOperationsService,
)


class FakeMessageOperationsService(MessageOperationsService):
    def __init__(self):
        super().__init__()
        self.added_messages = []
        self.updated_messages = []
        self.removed_messages = []
        self.expired_removed = False

    def add_message(self, message, message_collection, limits):
        self.added_messages.append(message)
        return message_collection.add_message(message)

    def update_message(
        self,
        message_id,
        message_collection,
        text=None,
        attachments=None,
        metadata=None,
        total_tokens=None,
    ):
        self.updated_messages.append(message_id)
        return message_collection

    def remove_message(self, message_id, message_collection):
        self.removed_messages.append(message_id)
        return message_collection

    def remove_expired_messages(self, message_collection, timeout):
        self.expired_removed = True
        return message_collection


def create_message(
    text="text",
    sender="user",
    role=None,
    parent_message_id=None,
    attachments=None,
    metadata=None,
    total_tokens=1,
):
    return Message(
        message_id=uuid4(),
        sender=sender,
        text=text,
        role=role,
        parent_message_id=parent_message_id,
        attachments=attachments or [],
        metadata=metadata or {},
        total_tokens=total_tokens,
    )


def create_context(
    message_service=None,
    message_collection=None,
    limits=None,
    created_at=None,
    updated_at=None,
):
    return ChatContext(
        context_id=uuid4(),
        agent_id=uuid4(),
        user_id=uuid4(),
        message_service=message_service or FakeMessageOperationsService(),
        message_collection=message_collection or MessageCollection(),
        limits=limits or ChatLimits(),
        created_at=created_at,
        updated_at=updated_at,
    )


def test_init_with_all_parameters():
    context_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()
    message_service = FakeMessageOperationsService()
    message_collection = MessageCollection()
    limits = ChatLimits(max_messages=10, max_tokens=100, timeout=60)
    created_at = datetime.now()
    updated_at = datetime.now()
    context = ChatContext(
        context_id,
        agent_id,
        user_id,
        message_service,
        message_collection,
        limits,
        created_at,
        updated_at,
    )
    assert context.context_id == context_id
    assert context.agent_id == agent_id
    assert context.user_id == user_id
    assert context._message_collection == message_collection
    assert context._limits == limits
    assert context._created_at == created_at
    assert context._updated_at == updated_at


def test_init_with_minimal_parameters():
    context = create_context()
    assert context._message_collection.total_messages == 0
    assert context._limits.max_messages is None
    assert context._created_at is not None
    assert context._updated_at is not None


def test_init_with_default_message_collection():
    context = create_context(message_collection=None)
    assert isinstance(context._message_collection, MessageCollection)


def test_init_with_default_limits():
    context = create_context(limits=None)
    assert isinstance(context._limits, ChatLimits)


def test_init_with_default_timestamps():
    context = create_context(created_at=None, updated_at=None)
    assert isinstance(context._created_at, datetime)
    assert isinstance(context._updated_at, datetime)


def test_init_with_custom_timestamps():
    now = datetime.now()
    context = create_context(created_at=now, updated_at=now)
    assert context._created_at == now
    assert context._updated_at == now


def test_context_id_property():
    context_id = uuid4()
    context = create_context()
    object.__setattr__(context, "_context_id", context_id)
    assert context.context_id == context_id


def test_agent_id_property():
    agent_id = uuid4()
    context = create_context()
    object.__setattr__(context, "_agent_id", agent_id)
    assert context.agent_id == agent_id


def test_user_id_property():
    user_id = uuid4()
    context = create_context()
    object.__setattr__(context, "_user_id", user_id)
    assert context.user_id == user_id


def test_created_at_property():
    now = datetime.now()
    context = create_context(created_at=now)
    assert context.created_at == now


def test_updated_at_property():
    now = datetime.now()
    context = create_context(updated_at=now)
    assert context.updated_at == now


def test_properties_immutability():
    context = create_context()
    with pytest.raises(AttributeError):
        context.context_id = uuid4()
    with pytest.raises(AttributeError):
        context.agent_id = uuid4()
    with pytest.raises(AttributeError):
        context.user_id = uuid4()
    with pytest.raises(AttributeError):
        context.created_at = datetime.now()
    with pytest.raises(AttributeError):
        context.updated_at = datetime.now()


def test_create_with_all_parameters():
    context_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()
    message_service = FakeMessageOperationsService()
    message_collection = MessageCollection()
    max_messages = 5
    max_tokens = 50
    timeout = 10
    created_at = datetime.now()
    context = ChatContext.create(
        context_id,
        agent_id,
        user_id,
        message_service,
        message_collection,
        max_messages,
        max_tokens,
        timeout,
        created_at,
    )
    assert context.context_id == context_id
    assert context.agent_id == agent_id
    assert context.user_id == user_id
    assert context._limits.max_messages == max_messages
    assert context._limits.max_tokens == max_tokens
    assert context._limits.timeout == timeout
    assert context._created_at == created_at


def test_create_with_minimal_parameters():
    context_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()
    message_service = FakeMessageOperationsService()
    context = ChatContext.create(
        context_id, agent_id, user_id, message_service
    )
    assert context.context_id == context_id
    assert context.agent_id == agent_id
    assert context.user_id == user_id
    assert context._limits.max_messages is None
    assert context._limits.max_tokens is None
    assert context._limits.timeout is None
    assert isinstance(context._created_at, datetime)


def test_create_with_custom_limits():
    context_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()
    message_service = FakeMessageOperationsService()
    max_messages = 3
    max_tokens = 30
    timeout = 5
    context = ChatContext.create(
        context_id,
        agent_id,
        user_id,
        message_service,
        max_messages=max_messages,
        max_tokens=max_tokens,
        timeout=timeout,
    )
    assert context._limits.max_messages == max_messages
    assert context._limits.max_tokens == max_tokens
    assert context._limits.timeout == timeout


def test_create_with_none_limits():
    context_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()
    message_service = FakeMessageOperationsService()
    context = ChatContext.create(
        context_id,
        agent_id,
        user_id,
        message_service,
        max_messages=None,
        max_tokens=None,
        timeout=None,
    )
    assert context._limits.max_messages is None
    assert context._limits.max_tokens is None
    assert context._limits.timeout is None


def test_create_with_custom_message_collection():
    context_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()
    message_service = FakeMessageOperationsService()
    message_collection = MessageCollection()
    context = ChatContext.create(
        context_id,
        agent_id,
        user_id,
        message_service,
        message_collection=message_collection,
    )
    assert context._message_collection == message_collection


def test_create_default_timestamp_generation():
    context_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()
    message_service = FakeMessageOperationsService()
    context = ChatContext.create(
        context_id, agent_id, user_id, message_service
    )
    assert isinstance(context._created_at, datetime)


def test_create_with_custom_timestamp():
    context_id = uuid4()
    agent_id = uuid4()
    user_id = uuid4()
    message_service = FakeMessageOperationsService()
    now = datetime.now()
    context = ChatContext.create(
        context_id, agent_id, user_id, message_service, created_at=now
    )
    assert context._created_at == now
