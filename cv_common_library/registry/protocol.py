from typing import Protocol, Any


class RegistryProtocol(Protocol):
    @classmethod
    def create_instance(cls) -> Any:
        """Create instance of the object."""
        ...
