from datetime import datetime
from uuid import uuid4

import pytest

from src.myjarvis.domain.exceptions import (
    MessageHasInvalidParentId,
    MessageNotFound,
    MessageCouldNotBeEmpty,
    MessageTooLong,
    WrongIdType,
)
from src.myjarvis.domain.services.message_operations_service import (
    MessageOperationsService,
)
from src.myjarvis.domain.value_objects import Message
from src.myjarvis.domain.value_objects.chat_limits import ChatLimits as CL
from src.myjarvis.domain.value_objects.message_collection import (
    MessageCollection as MC,
)
from src.myjarvis.domain.value_objects.message_role import MessageRole


class FakeLimitsService:
    def apply_limits(self, messages, limits):
        if limits is None:
            return messages
        if limits.max_messages is not None:
            messages = messages[-limits.max_messages :]
        if limits.max_tokens is not None:
            total = 0
            result = []
            for m in reversed(messages):
                total += m.total_tokens
                if total > limits.max_tokens:
                    break
                result.append(m)
            messages = list(reversed(result))
        return messages


class FakeExpirationService:
    def remove_expired_messages(self, message_collection, timeout):
        return message_collection


class FakeChatContextServices:
    def __init__(self):
        self.limits_service = FakeLimitsService()
        self.expiration_service = FakeExpirationService()


class FakeMessage(Message):
    def __init__(
        self,
        message_id=None,
        sender=None,
        text="text",
        timestamp=None,
        role=None,
        parent_message_id=None,
        attachments=None,
        metadata=None,
        total_tokens=1,
        max_text_length=1000,
    ):
        super().__init__(
            message_id=message_id or uuid4(),
            sender=sender or uuid4(),
            text=text,
            timestamp=timestamp or datetime.now(),
            role=role or MessageRole.USER,
            parent_message_id=parent_message_id,
            attachments=attachments or [],
            metadata=metadata or {},
            total_tokens=total_tokens,
            max_text_length=max_text_length,
        )


def make_collection(messages=None):
    return MC.create(messages or [])


def make_limits(max_messages=None, max_tokens=None, timeout=None):
    return CL.create(max_messages, max_tokens, timeout)


@pytest.fixture
def service():
    return MessageOperationsService(FakeChatContextServices())


@pytest.fixture
def msg():
    return FakeMessage()


@pytest.fixture
def msg2():
    return FakeMessage()


@pytest.fixture
def msg3():
    return FakeMessage()


def test_get_message_found(service, msg):
    c = make_collection([msg])
    assert service.get_message(msg.message_id, c) == msg


def test_get_message_not_found(service, msg):
    c = make_collection([msg])
    assert service.get_message(uuid4(), c) is None


def test_get_message_empty(service):
    c = make_collection()
    assert service.get_message(uuid4(), c) is None


def test_get_message_invalid_uuid(service, msg):
    c = make_collection([msg])
    assert service.get_message(uuid4(), c) is None


def test_add_message_no_parent(service, msg):
    c = make_collection()
    result = service.add_message(msg, c, None)
    assert msg.message_id in result.messages


def test_add_message_with_parent(service, msg, msg2):
    c = make_collection([msg])
    child = FakeMessage(parent_message_id=msg.message_id)
    result = service.add_message(child, c, None)
    assert child.message_id in result.messages


def test_add_message_with_limits(service, msg, msg2):
    c = make_collection([msg, msg2])
    m = FakeMessage()
    limits = make_limits(max_messages=2)
    result = service.add_message(m, c, limits)
    assert len(result.messages) == 2


def test_add_message_no_limits(service, msg):
    c = make_collection([msg])
    m = FakeMessage()
    result = service.add_message(m, c, None)
    assert m.message_id in result.messages


def test_add_message_invalid_parent(service, msg):
    c = make_collection([msg])
    m = FakeMessage(parent_message_id=uuid4())
    with pytest.raises(MessageHasInvalidParentId):
        service.add_message(m, c, None)


def test_add_message_non_uuid_parent_id(service, msg):
    with pytest.raises(WrongIdType):
        FakeMessage(parent_message_id="not-a-uuid")


def test_add_message_empty_collection(service, msg):
    c = make_collection()
    result = service.add_message(msg, c, None)
    assert msg.message_id in result.messages


def test_add_message_reach_limits(service, msg, msg2):
    c = make_collection([msg, msg2])
    m = FakeMessage()
    limits = make_limits(max_messages=2)
    result = service.add_message(m, c, limits)
    assert len(result.messages) == 2


def test_add_message_long_text(service, msg):
    c = make_collection([msg])
    m = FakeMessage(text="x" * 10000, max_text_length=None)
    result = service.add_message(m, c, None)
    assert m.message_id in result.messages


def test_add_message_multiple_attachments(service, msg):
    c = make_collection([msg])
    m = FakeMessage(attachments=[1, 2, 3])
    result = service.add_message(m, c, None)
    assert m.message_id in result.messages


def test_add_message_extreme_total_tokens(service, msg):
    c = make_collection([msg])
    m = FakeMessage(total_tokens=999999)
    result = service.add_message(m, c, None)
    assert m.message_id in result.messages


def test_update_message_success(service, msg):
    c = make_collection([msg])
    result = service.update_message(msg.message_id, c, text="new")
    assert result.get_message(msg.message_id).text == "new"


def test_update_message_only_text(service, msg):
    c = make_collection([msg])
    result = service.update_message(msg.message_id, c, text="t")
    assert result.get_message(msg.message_id).text == "t"


def test_update_message_only_attachments(service, msg):
    c = make_collection([msg])
    result = service.update_message(msg.message_id, c, attachments=[1])
    assert result.get_message(msg.message_id).attachments == [1]


def test_update_message_only_metadata(service, msg):
    c = make_collection([msg])
    result = service.update_message(msg.message_id, c, metadata={"a": 1})
    assert result.get_message(msg.message_id).metadata == {"a": 1}


def test_update_message_only_total_tokens(service, msg):
    c = make_collection([msg])
    result = service.update_message(msg.message_id, c, total_tokens=42)
    assert result.get_message(msg.message_id).total_tokens == 42


def test_update_message_all_fields(service, msg):
    c = make_collection([msg])
    result = service.update_message(
        msg.message_id,
        c,
        text="t",
        attachments=[1],
        metadata={"a": 1},
        total_tokens=2,
    )
    m = result.get_message(msg.message_id)
    assert (
        m.text == "t"
        and m.attachments == [1]
        and m.metadata == {"a": 1}
        and m.total_tokens == 2
    )


def test_update_message_none_fields(service, msg):
    c = make_collection([msg])
    result = service.update_message(msg.message_id, c)
    m = result.get_message(msg.message_id)
    assert (
        m.text == msg.text
        and m.attachments == msg.attachments
        and m.metadata == msg.metadata
        and m.total_tokens == msg.total_tokens
    )


def test_update_message_not_found(service, msg):
    c = make_collection([msg])
    with pytest.raises(MessageNotFound):
        service.update_message(uuid4(), c, text="x")


def test_update_message_empty_collection(service):
    c = make_collection()
    with pytest.raises(MessageNotFound):
        MessageOperationsService.update_message(uuid4(), c, text="x")


def test_update_message_empty_values(service, msg):
    c = make_collection([msg])
    with pytest.raises(MessageCouldNotBeEmpty):
        service.update_message(
            msg.message_id,
            c,
            text="",
            attachments=[],
            metadata={},
            total_tokens=0,
        )


def test_update_message_immutable_fields(service, msg):
    c = make_collection([msg])
    result = service.update_message(msg.message_id, c)
    m = result.get_message(msg.message_id)
    assert (
        m.message_id == msg.message_id
        and m.sender == msg.sender
        and m.timestamp == msg.timestamp
        and m.role == msg.role
        and m.parent_message_id == msg.parent_message_id
    )


def test_remove_message_success(service, msg):
    c = make_collection([msg])
    result = service.remove_message(msg.message_id, c)
    assert msg.message_id not in result.messages


def test_remove_message_not_found(service, msg):
    c = make_collection([msg])
    with pytest.raises(MessageNotFound):
        service.remove_message(uuid4(), c)


def test_remove_message_empty_collection(service):
    c = make_collection()
    with pytest.raises(MessageNotFound):
        service.remove_message(uuid4(), c)


def test_remove_message_last(service, msg):
    c = make_collection([msg])
    result = service.remove_message(msg.message_id, c)
    assert len(result.messages) == 0


def test_remove_multiple_messages_success(service, msg, msg2, msg3):
    c = make_collection([msg, msg2, msg3])
    result = service.remove_multiple_messages(
        [msg.message_id, msg2.message_id], c
    )
    assert (
        msg.message_id not in result.messages
        and msg2.message_id not in result.messages
    )


def test_remove_multiple_messages_mixed(service, msg, msg2):
    c = make_collection([msg, msg2])
    with pytest.raises(MessageNotFound):
        service.remove_multiple_messages([msg.message_id, uuid4()], c)


def test_remove_multiple_messages_empty_list(service, msg):
    c = make_collection([msg])
    result = service.remove_multiple_messages([], c)
    assert result.messages == c.messages


def test_remove_multiple_messages_all_not_exist(service, msg):
    c = make_collection([msg])
    result = service.remove_multiple_messages([uuid4(), uuid4()], c)
    assert result.messages == c.messages


def test_remove_multiple_messages_duplicates(service, msg, msg2):
    c = make_collection([msg, msg2])
    with pytest.raises(MessageNotFound):
        service.remove_multiple_messages([msg.message_id, msg.message_id], c)


def test_remove_multiple_messages_all(service, msg, msg2):
    c = make_collection([msg, msg2])
    result = service.remove_multiple_messages(
        [msg.message_id, msg2.message_id], c
    )
    assert len(result.messages) == 0


def test_message_creation_exceeds_max_text_length():
    max_text_length = 1000
    long_text = "x" * (max_text_length + 1)
    with pytest.raises(MessageTooLong):
        FakeMessage(text=long_text, max_text_length=max_text_length)
