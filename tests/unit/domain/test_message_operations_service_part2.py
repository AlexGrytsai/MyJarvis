from datetime import datetime, timedelta
from uuid import uuid4

from src.myjarvis.domain.services.chat_context_services import (
    ChatContextServices,
)
from src.myjarvis.domain.services.message_operations_service import (
    MessageOperationsService,
)
from src.myjarvis.domain.value_objects.chat_limits import ChatLimits
from src.myjarvis.domain.value_objects.message import Message
from src.myjarvis.domain.value_objects.message_collection import (
    MessageCollection,
)
from src.myjarvis.domain.value_objects.message_role import MessageRole


class FakeExpirationService:
    def remove_expired_messages(self, message_collection, timeout):
        if timeout is None or timeout <= 0:
            return message_collection
        now = datetime.now()
        filtered = [
            m
            for m in message_collection.messages.values()
            if (now - m.timestamp).total_seconds() <= timeout
        ]
        return message_collection.create(filtered)


class FakeLimitsService:
    def apply_limits(self, messages, limits):
        if limits.max_messages:
            messages = messages[-limits.max_messages :]
        if limits.max_tokens:
            total = 0
            result = []
            for m in reversed(messages):
                total += m.total_tokens
                if total > limits.max_tokens:
                    break
                result.append(m)
            messages = list(reversed(result))
        return messages


class FakeChatContextServices(ChatContextServices):
    @classmethod
    def create_default(cls):
        return cls(FakeLimitsService(), FakeExpirationService())

    @classmethod
    def create(cls, limits_service, expiration_service):
        return cls(limits_service, expiration_service)


def make_message(
    ts=None,
    parent=None,
    text=None,
    mid=None,
    tokens=1,
    attachments=None,
    role=MessageRole.USER,
):
    return Message(
        message_id=mid or uuid4(),
        sender="user",
        text=text or "msg",
        timestamp=ts or datetime.now(),
        role=role,
        parent_message_id=parent,
        attachments=attachments or [],
        metadata={},
        total_tokens=tokens,
    )


def make_collection(messages):
    return MessageCollection.create(messages)


def test_remove_expired_messages_removes_expired():
    s = MessageOperationsService(FakeChatContextServices.create_default())
    old = datetime.now() - timedelta(seconds=100)
    m1 = make_message(ts=old)
    m2 = make_message()
    c = make_collection([m1, m2])
    result = s.remove_expired_messages(c, 10)
    assert m1.message_id not in result.messages
    assert m2.message_id in result.messages


def test_remove_expired_messages_none_timeout():
    s = MessageOperationsService(FakeChatContextServices.create_default())
    m = make_message()
    c = make_collection([m])
    result = s.remove_expired_messages(c, None)
    assert result == c


def test_remove_expired_messages_zero_timeout():
    s = MessageOperationsService(FakeChatContextServices.create_default())
    m = make_message()
    c = make_collection([m])
    result = s.remove_expired_messages(c, 0)
    assert result == c


def test_remove_expired_messages_negative_timeout():
    s = MessageOperationsService(FakeChatContextServices.create_default())
    m = make_message()
    c = make_collection([m])
    result = s.remove_expired_messages(c, -1)
    assert result == c


def test_remove_expired_messages_large_timeout():
    s = MessageOperationsService(FakeChatContextServices.create_default())
    m = make_message(ts=datetime.now() - timedelta(days=1))
    c = make_collection([m])
    result = s.remove_expired_messages(c, 999999)
    assert m.message_id in result.messages


def test_remove_expired_messages_no_expired():
    s = MessageOperationsService(FakeChatContextServices.create_default())
    m = make_message()
    c = make_collection([m])
    result = s.remove_expired_messages(c, 100)
    assert result.messages == c.messages


def test_check_parent_message_exists_none():
    m = make_message()
    c = make_collection([m])
    assert MessageOperationsService._check_parent_message_exists(None, c)


def test_check_parent_message_exists_exists():
    m = make_message()
    c = make_collection([m])
    assert MessageOperationsService._check_parent_message_exists(
        m.message_id, c
    )


def test_check_parent_message_exists_not_exists():
    m = make_message()
    c = make_collection([m])
    fake_id = uuid4()
    assert not MessageOperationsService._check_parent_message_exists(
        fake_id, c
    )


def test_check_parent_message_exists_empty():
    c = make_collection([])
    assert not MessageOperationsService._check_parent_message_exists(
        uuid4(), c
    )


def test_check_parent_message_exists_invalid_uuid():
    c = make_collection([])
    assert not MessageOperationsService._check_parent_message_exists(
        uuid4(), c
    )


def test_filter_existing_message_ids_all_exist():
    m1 = make_message()
    m2 = make_message()
    c = make_collection([m1, m2])
    ids = [m1.message_id, m2.message_id]
    result = MessageOperationsService._filter_existing_message_ids(ids, c)
    assert set(result) == set(ids)


def test_filter_existing_message_ids_none_exist():
    c = make_collection([])
    ids = [uuid4(), uuid4()]
    result = MessageOperationsService._filter_existing_message_ids(ids, c)
    assert result == []


def test_filter_existing_message_ids_mixed():
    m = make_message()
    c = make_collection([m])
    ids = [m.message_id, uuid4()]
    result = MessageOperationsService._filter_existing_message_ids(ids, c)
    assert result == [m.message_id]


def test_filter_existing_message_ids_empty():
    c = make_collection([])
    result = MessageOperationsService._filter_existing_message_ids([], c)
    assert result == []


def test_filter_existing_message_ids_duplicates():
    m = make_message()
    c = make_collection([m])
    ids = [m.message_id, m.message_id]
    result = MessageOperationsService._filter_existing_message_ids(ids, c)
    assert result == [m.message_id, m.message_id]


def test_filter_existing_message_ids_empty_collection():
    c = make_collection([])
    ids = [uuid4()]
    result = MessageOperationsService._filter_existing_message_ids(ids, c)
    assert result == []


def test_init_with_custom_services():
    limits = FakeLimitsService()
    expiration = FakeExpirationService()
    services = FakeChatContextServices.create(limits, expiration)
    s = MessageOperationsService(services)
    assert s._services.limits_service is limits
    assert s._services.expiration_service is expiration


def test_init_with_default_services():
    s = MessageOperationsService()
    assert hasattr(s._services, "limits_service")
    assert hasattr(s._services, "expiration_service")


def test_limits_service_applied():
    class CustomLimitsService(FakeLimitsService):
        def apply_limits(self, messages, limits):
            return []

    services = FakeChatContextServices.create(
        CustomLimitsService(), FakeExpirationService()
    )
    s = MessageOperationsService(services)
    m = make_message()
    c = make_collection([m])
    limits = ChatLimits(max_messages=1)
    result = s.add_message(m, c, limits)
    assert result.total_messages == 0


def test_expiration_service_applied():
    class CustomExpirationService(FakeExpirationService):
        def remove_expired_messages(self, message_collection, timeout):
            return message_collection.create([])

    services = FakeChatContextServices.create(
        FakeLimitsService(), CustomExpirationService()
    )
    s = MessageOperationsService(services)
    m = make_message()
    c = make_collection([m])
    result = s.remove_expired_messages(c, 1)
    assert result.total_messages == 0


def test_large_collection_operations():
    s = MessageOperationsService(FakeChatContextServices.create_default())
    messages = [
        make_message(ts=datetime.now() - timedelta(seconds=i), tokens=2)
        for i in range(1200)
    ]
    c = make_collection(messages)
    limits = ChatLimits(max_messages=1000)
    m = make_message()
    c2 = s.add_message(m, c, limits)
    assert c2.total_messages <= 1000
    result = s.remove_expired_messages(c2, 100000)
    assert result.total_messages <= 1000


def test_add_message_with_large_attachments():
    s = MessageOperationsService(FakeChatContextServices.create_default())
    big_attachment = [b"x" * 1000000]
    m = make_message(attachments=big_attachment)
    c = make_collection([])
    limits = ChatLimits(max_messages=10)
    c2 = s.add_message(m, c, limits)
    assert m.message_id in c2.messages


def test_mass_remove_messages():
    s = MessageOperationsService(FakeChatContextServices.create_default())
    messages = [make_message() for _ in range(100)]
    c = make_collection(messages)
    ids = [m.message_id for m in messages[:50]]
    c2 = s.remove_multiple_messages(ids, c)
    assert all(mid not in c2.messages for mid in ids)
    assert len(c2.messages) == 50


def test_search_in_large_collection():
    s = MessageOperationsService(FakeChatContextServices.create_default())
    messages = [make_message(text=f"msg{i}") for i in range(1000)]
    c = make_collection(messages)
    mid = messages[500].message_id
    found = s.get_message(mid, c)
    assert found is not None
    assert found.text == "msg500"
