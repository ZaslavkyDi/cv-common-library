from typing import Self

import pytest

from cv_common_library.registry.registry import Registry


class FakeService:
    def __init__(self, value: str):
        self.value: str = value

    @classmethod
    def create_instance(cls) -> Self:
        return cls(value="Test Value")


service_registry: Registry[str, FakeService] = Registry()


@pytest.fixture(scope="function", autouse=True)
def setup_registry() -> None:
    @service_registry.register("service1")
    class FakeService1(FakeService):
        ...

    @service_registry.register("service2")
    class FakeService2(FakeService):
        @classmethod
        def create_instance(cls) -> Self:
            return cls(value="Not a test value")

    yield

    service_registry._registry = {}


def test_register() -> None:
    assert service_registry.keys() == {"service1", "service2"}
    assert service_registry.get("service1").value == "Test Value"
    assert service_registry.get("service2").value == "Not a test value"

    assert isinstance(service_registry.get("service1"), FakeService)


def test_registry_class_with_wrong_type() -> None:
    @service_registry.register("wrong_type")
    class WrongType:
        @classmethod
        def create_instance(cls) -> Self:
            return cls()

    assert service_registry.get("wrong_type") is not None


def test_registry_class_with_no_protocol_method() -> None:
    with pytest.raises(AttributeError):

        @service_registry.register("wrong_method")
        class WrongMethod:
            ...
