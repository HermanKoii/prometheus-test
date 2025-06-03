import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv


class ConfigurationError(Exception):
    """Custom exception for configuration loading errors."""
    pass


def load_config(config_file: Optional[str] = None) -> Dict[str, Any]:
    """
    Load configuration from environment variables or a specified config file.

    Args:
        config_file (Optional[str]): Path to an optional configuration file.

    Returns:
        Dict[str, Any]: Loaded configuration dictionary.

    Raises:
        ConfigurationError: If required configuration is missing or invalid.
    """
    # Load .env file if specified or default .env exists
    if config_file:
        load_dotenv(config_file)
    else:
        load_dotenv()

    # Configuration dictionary to store loaded settings
    config = {
        'api_base_url': os.getenv('COINGECKO_API_BASE_URL', 'https://api.coingecko.com/api/v3'),
        'api_key': os.getenv('COINGECKO_API_KEY', ''),
        'request_timeout': int(os.getenv('COINGECKO_REQUEST_TIMEOUT', 30)),
        'max_retries': int(os.getenv('COINGECKO_MAX_RETRIES', 3)),
        'rate_limit_delay': int(os.getenv('COINGECKO_RATE_LIMIT_DELAY', 1))
    }

    # Validate critical configuration
    _validate_config(config)

    return config


def _validate_config(config: Dict[str, Any]) -> None:
    """
    Validate the loaded configuration.

    Args:
        config (Dict[str, Any]): Configuration dictionary to validate.

    Raises:
        ConfigurationError: If configuration is invalid.
    """
    # Basic validation rules
    if not config['api_base_url']:
        raise ConfigurationError("Invalid or missing API base URL")

    if config['request_timeout'] <= 0:
        raise ConfigurationError("Request timeout must be a positive integer")

    if config['max_retries'] < 0:
        raise ConfigurationError("Max retries cannot be negative")