import logging
from typing import Any, Dict, List, Optional, TypeVar, Union, Callable

from .config_exceptions import ConfigValueNotFoundException
from .config_interfaces import ConfigSource, SecretSource

T = TypeVar('T')

logger = logging.getLogger(__name__)


class ConfigurationManager:
    """
    Manages configuration retrieval from multiple sources with a defined precedence.

    Configuration sources are checked in the order they are provided, and the first
    value found is returned. If a secret is requested, the secret source is checked
    after the regular configuration sources.
    """

    def __init__(
            self,
            config_sources: List[ConfigSource],
            secret_sources: List[SecretSource]
    ) -> None:
        """
        Initialize the configuration manager.

        Args:
            config_sources: List of configuration sources in order of precedence
            secret_source: List of secret sources in order of precedence
        """
        self._config_sources = config_sources
        self._secret_sources = secret_sources

    def _get_from_sources(self, key, sources, is_secret=False, context=None, source_type='config'):
        for source in sources:
            value = source.get_value(key, context)
            if value is not None:
                logger.debug(f"Found value for {'key' if source_type=='config' else 'secret'} '{key}' in {source.__class__.__name__}")
                return source, value
        return None, None

    def get(
            self,
            key: str,
            default: Optional[T] = None,
            is_secret: bool = False,
            context: Dict[str, Any] = None,
            value_processor : Callable[[ConfigSource, Any], T] = None
    ) -> Union[T, Any]:
        """
        Get a configuration value.

        Args:
            key: The configuration key
            default: Default value if not found
            is_secret: Whether the value is a secret
            context: Additional context for configuration sources
            value_processor: function to convert the value

        Returns:
            The configuration value

        Raises:
            ConfigValueNotFoundException: If value not found and no default provided
            SecretNotFoundException: If secret not found and no default provided.
        """

        # First check configuration sources
        if not is_secret:
            source, value = self._get_from_sources(key, self._config_sources, is_secret, context, 'config')
        else:
            # If it's a secret, check the secret source
            source, value = self._get_from_sources(key, self._secret_sources, is_secret, context, 'secret')
        if value is not None:
            if value_processor is not None:
                return value_processor(source, value)
            return value

        # Return default or raise exception
        if default is not None:
            logger.debug(f"Using default value for key '{key}'")
            return default

        # Raise appropriate exception
        raise ConfigValueNotFoundException(key, context)