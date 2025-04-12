from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, TypeVar, Generic

T = TypeVar('T')


class ConfigSource(ABC):
    """Interface for configuration sources."""

    @abstractmethod
    def get_value(self, key: str, context: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        """
        Retrieve a configuration value.

        Args:
            key: The configuration key to retrieve
            context: Additional context that might be needed to retrieve the value

        Returns:
            The configuration value or None if not found
        """
        pass


class SecretSource(ConfigSource, ABC):
    """Interface for secret sources."""


class TypeConverter(Generic[T], ABC):
    """Interface for type conversion of configuration values."""

    @abstractmethod
    def convert(self, value: Any) -> T:
        """
        Convert a value to the target type.

        Args:
            value: The value to convert

        Returns:
            The converted value

        Raises:
            ValueError: If the value cannot be converted
        """
        pass