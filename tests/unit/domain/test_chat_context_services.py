from dataclasses import FrozenInstanceError

import pytest

from src.myjarvis.domain.exceptions.domain_exceptions import (
    InvalidChatContextServiceError,
)
from src.myjarvis.domain.services.chat_context_services import (
    ChatContextServices,
)
from src.myjarvis.domain.services.chat_limits_service import (
    ChatContextLimitsService,
)
from src.myjarvis.domain.services.message_expiration_service import (
    MessageExpirationService,
)


class FakeLimitsService(ChatContextLimitsService):
    def __init__(self):
        self.fake = True


class FakeExpirationService(MessageExpirationService):
    def __init__(self):
        self.fake = True


def test_chat_context_services_initialization():
    limits = FakeLimitsService()
    expiration = FakeExpirationService()
    services = ChatContextServices(limits, expiration)
    assert services.limits_service is limits
    assert services.expiration_service is expiration
    assert hasattr(services, "limits_service")
    assert hasattr(services, "expiration_service")
    with pytest.raises(FrozenInstanceError):
        services.limits_service = None


def test_chat_context_services_slots():
    limits = FakeLimitsService()
    expiration = FakeExpirationService()
    services = ChatContextServices(limits, expiration)
    with pytest.raises(TypeError):
        services.new_attr = 123


def test_create_with_valid_services():
    limits = FakeLimitsService()
    expiration = FakeExpirationService()
    services = ChatContextServices.create(limits, expiration)
    assert services.limits_service is limits
    assert services.expiration_service is expiration


def test_create_returns_new_instance():
    limits = FakeLimitsService()
    expiration = FakeExpirationService()
    s1 = ChatContextServices.create(limits, expiration)
    s2 = ChatContextServices.create(limits, expiration)
    assert s1 is not s2
    assert id(s1) != id(s2)


def test_create_default_services_types():
    services = ChatContextServices.create_default()
    assert isinstance(services.limits_service, ChatContextLimitsService)
    assert isinstance(services.expiration_service, MessageExpirationService)


def test_create_default_limits_service_strategies():
    services = ChatContextServices.create_default()
    strategies = getattr(services.limits_service, "strategies", None)
    assert strategies is not None
    names = {type(s).__name__ for s in strategies}
    assert "MaxMessagesLimitStrategy" in names
    assert "MaxTokensLimitStrategy" in names


def test_create_default_expiration_service_config():
    services = ChatContextServices.create_default()
    expiration_service = services.expiration_service
    assert isinstance(expiration_service, MessageExpirationService)
    assert hasattr(expiration_service, "_expiration_strategy")


def test_create_default_returns_new_instance_each_time():
    s1 = ChatContextServices.create_default()
    s2 = ChatContextServices.create_default()
    assert s1 is not s2
    assert id(s1) != id(s2)
    assert s1.limits_service is not s2.limits_service
    assert s1.expiration_service is not s2.expiration_service


def test_create_with_fake_services():
    limits = FakeLimitsService()
    expiration = FakeExpirationService()
    services = ChatContextServices.create(limits, expiration)
    assert services.limits_service is limits
    assert services.expiration_service is expiration


def test_create_with_same_service_instance():
    fake = FakeLimitsService()
    services = ChatContextServices.create(fake, fake)
    assert services.limits_service is fake
    assert services.expiration_service is fake


def test_dataclass_equality():
    limits1 = FakeLimitsService()
    expiration1 = FakeExpirationService()
    limits2 = FakeLimitsService()
    expiration2 = FakeExpirationService()
    s1 = ChatContextServices.create(limits1, expiration1)
    s2 = ChatContextServices.create(limits1, expiration1)
    s3 = ChatContextServices.create(limits2, expiration2)
    assert s1 == s2
    assert s1 != s3
    assert hash(s1) == hash(s2)


def test_dataclass_immutability():
    limits = FakeLimitsService()
    expiration = FakeExpirationService()
    services = ChatContextServices.create(limits, expiration)
    with pytest.raises(FrozenInstanceError):
        services.limits_service = None


def test_repr_and_str():
    limits = FakeLimitsService()
    expiration = FakeExpirationService()
    services = ChatContextServices.create(limits, expiration)
    s = str(services)
    r = repr(services)
    assert "ChatContextServices" in s
    assert "ChatContextServices" in r


def test_thread_safety():
    import threading

    results = []

    def worker():
        results.append(ChatContextServices.create_default())

    threads = [threading.Thread(target=worker) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert len(results) == 10
    assert all(isinstance(s, ChatContextServices) for s in results)


def test_create_with_none_limits_service():
    expiration = FakeExpirationService()
    with pytest.raises(InvalidChatContextServiceError):
        ChatContextServices.create(None, expiration)


def test_create_with_none_expiration_service():
    limits = FakeLimitsService()
    with pytest.raises(InvalidChatContextServiceError):
        ChatContextServices.create(limits, None)


def test_create_with_both_none_services():
    with pytest.raises(InvalidChatContextServiceError):
        ChatContextServices.create(None, None)
