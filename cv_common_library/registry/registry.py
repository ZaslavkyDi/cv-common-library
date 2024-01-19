from typing import Callable

from cv_common_library.registry.protocol import RegistryProtocol


class Registry[_K, _V: RegistryProtocol](dict[_K, _V]):
    """
    Usage:
    service_registry: Registry[str, FakeService] = Registry()
    """

    def register(self, qualifier: _K) -> Callable[[_V], _V]:
        def decorator(_cls: _V) -> _V:
            self[qualifier] = _cls.create_instance()
            return _cls

        return decorator
