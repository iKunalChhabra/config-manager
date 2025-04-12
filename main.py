import logging

from config import ConfigurationFactory
from config.config_exceptions import ConfigException
from config.config_sources import EnvironmentSource

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Main application entry point."""
    try:
        # Create configuration manager
        config = ConfigurationFactory.create_default_manager()

        # Example usage
        try:
            all_tables = config.get("all_tables")
            logger.info(f"All tables: {all_tables}")

            all_columns = config.get("all_columns", context={"table_id": "t1"}, value_processor=lambda src,v: v.split(",") if isinstance(src, EnvironmentSource) else v)
            logger.info(f"Columns for t1: {all_columns} with type {type(all_columns)}")

            password = config.get("password", is_secret=True)
            logger.info(f"Password retrieved {password}")

            env = config.get("env")
            logger.info(f"Current environment: {env}")

            # This will use the default value
            timeout = config.get("connection_timeout", default=30)
            logger.info(f"Connection timeout: {timeout}")

            # This will raise an exception
            non_existent = config.get("non_existent_value")
            logger.info(f"Non-existent value: {non_existent}")
        except ConfigException as e:
            logger.error(f"Configuration error: {e}")

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()