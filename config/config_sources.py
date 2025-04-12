import os
from datetime import datetime
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv

from .config_interfaces import ConfigSource, SecretSource

load_dotenv()


class EnvironmentSource(ConfigSource):
    """Configuration source that reads from environment variables."""

    def get_value(self, key: str, context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Retrieve a configuration value from environment variables.

        Args:
            key: The environment variable name
            context: Not used for environment variables

        Returns:
            The environment variable value or None if not set
        """
        return os.environ.get(key)


class BaseConfigSource(ConfigSource):
    """Configuration source that provides base configuration values."""

    def get_value(self, key: str, context: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        """
        Retrieve a base configuration value.

        Args:
            key: The configuration key (mapped to get_{key} method)
            context: Additional parameters to pass to the method

        Returns:
            The configuration value or None if method doesn't exist
        """
        method_name = f"get_{key}"
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            if context:
                valid_kwargs = {k: v for k, v in context.items() if k in method.__code__.co_varnames}
                return method(**valid_kwargs)
            return method()
        return None

    def get_env(self) -> str:
        """Get the current environment."""
        return 'PROD'

    def get_current_time(self) -> datetime:
        """Get the current time."""
        return datetime.now()


class MetadataSource(ConfigSource):
    """Configuration source that provides metadata."""

    def get_value(self, key: str, context: Optional[Dict[str, Any]] = None) -> Optional[Any]:
        """
        Retrieve metadata.

        Args:
            key: The metadata key (mapped to get_{key} method)
            context: Additional parameters to pass to the method

        Returns:
            The metadata or None if method doesn't exist
        """
        method_name = f"get_{key}"
        if hasattr(self, method_name):
            method = getattr(self, method_name)
            if context:
                valid_kwargs = {k: v for k, v in context.items() if k in method.__code__.co_varnames}
                return method(**valid_kwargs)
            return method()
        return None

    def get_all_tables(self) -> List[str]:
        """Get all available tables."""
        return ['t1', 't2', 't3']

    def get_all_columns(self, table_id: str) -> List[str]:
        """
        Get all columns for a table.

        Args:
            table_id: The table ID or None for all columns

        Returns:
            List of column names
        """
        if table_id == 't1':
            return ['c1', 'c2', 'c3']
        return []


class VaultSource(SecretSource):
    """Secret source that retrieves secrets from a vault."""

    def get_value(self, key: str, context: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """
        Retrieve a secret from the vault.

        Args:
            key: The secret key
            context: Additional parameters to pass to the method

        Returns:
            The secret value or None if not found
        """
        if key == "password":
            return "regergerg"
        return None