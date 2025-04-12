from typing import List

from .config_interfaces import ConfigSource, SecretSource
from .config_manager import ConfigurationManager
from .config_sources import (
    EnvironmentSource,
    BaseConfigSource,
    MetadataSource,
    VaultSource
)


class ConfigurationFactory:
    """Factory for creating configuration managers with standard sources."""

    @staticmethod
    def create_default_manager() -> ConfigurationManager:
        """
        Create a configuration manager with the default sources.

        Returns:
            ConfigurationManager instance with standard configuration
        """
        config_sources: List[ConfigSource] = [
            EnvironmentSource(),
            BaseConfigSource(),
            MetadataSource()
        ]

        secret_source: List[SecretSource ]= [
            EnvironmentSource(),
            VaultSource()
        ]

        return ConfigurationManager(config_sources, secret_source)