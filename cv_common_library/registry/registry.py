from typing import Callable

from cv_common_library.registry.protocol import RegistryProtocol


class Registry[_KT, _VT: RegistryProtocol](dict[_KT, _VT]):
    """
    Usage:
    service_registry: Registry[str, FakeService] = Registry()
    """

    def register(self, qualifier: _KT) -> Callable[[_VT], _VT]:
        def decorator(_cls: _VT) -> _VT:
            self[qualifier] = _cls.create_instance()
            return _cls

        return decorator
