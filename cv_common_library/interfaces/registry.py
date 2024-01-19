import abc
from collections.abc import Collection
from typing import Protocol, Any


class RegistryProtocol(Protocol):
    @classmethod
    def register(cls, *args: Any, **kwargs: Any) -> Any:
        """Register consumer in the registry."""
        ...

    def get(self, *args: Any, **kwargs: Any) -> Any:
        """Return object from the registry."""
        ...

    def get_all(self, *args: Any, **kwargs: Any) -> Collection[Any]:
        """Return all objects from the registry."""
        ...

    def get_names(self, *args: Any, **kwargs: Any) -> set[str]:
        """Return all names from the registry."""
        ...


class Registry[T](metaclass=abc.ABCMeta, RegistryProtocol):
    _registry: dict[str, T] = {}

    @classmethod
    def register(cls, qualifier: str, *args, **kwargs):
        def decorator(fun):
            def wrapper(*args, **kwargs):
                """Register consumer in the registry."""
                consumer = fun(*args, **kwargs)
                cls._registry[qualifier] = consumer

            return wrapper
        return decorator

    def get(self, qualifier: str, *args: Any, **kwargs: Any) -> T:
        return self._registry[qualifier]

    def get_all(self, *args: Any, **kwargs: Any) -> Collection[T]:
        return list(self._registry.values())

    def get_names(self, *args: Any, **kwargs: Any) -> set[str]:
        return set(self._registry.keys())
