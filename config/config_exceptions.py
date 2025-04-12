from typing import Any, Optional, Dict


class ConfigException(Exception):
    """Base exception for all configuration-related errors."""
    pass


class ConfigValueNotFoundException(ConfigException):
    """Raised when a configuration value cannot be found."""
    def __init__(self, key: str, context: Optional[Dict[str, Any]] = None) -> None:
        context_str = f" with context {context}" if context else ""
        super().__init__(f"Configuration value with key '{key}'{context_str} not found")


class SecretNotFoundException(ConfigException):
    """Raised when a secret cannot be found."""
    def __init__(self, key: str) -> None:
        super().__init__(f"Secret with key '{key}' not found")