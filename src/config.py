import os
from typing import Dict, Any, Optional
import json
from pathlib import Path

class ConfigurationError(Exception):
    """Custom exception for configuration loading errors."""
    pass

def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Load CoinGecko API configuration from environment variables or a config file.

    Args:
        config_path (Optional[str]): Path to the configuration file. Defaults to None.

    Returns:
        Dict[str, Any]: Loaded configuration dictionary.

    Raises:
        ConfigurationError: If configuration cannot be loaded or validated.
    """
    # Priority: Environment Variables > Config File > Default Values
    config = {}

    # Try environment variables
    env_api_key = os.getenv('COINGECKO_API_KEY')
    if env_api_key:
        config['api_key'] = env_api_key
    
    # Try config file if path is provided
    if config_path:
        try:
            config.update(_load_config_file(config_path))
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ConfigurationError(f"Error loading config file: {e}")

    # Set default values for missing configurations
    config.setdefault('base_url', 'https://api.coingecko.com/api/v3')
    config.setdefault('timeout', 10)
    config.setdefault('max_retries', 3)

    # Validate configuration
    _validate_config(config)

    return config

def _load_config_file(config_path: str) -> Dict[str, Any]:
    """
    Load configuration from a JSON file.

    Args:
        config_path (str): Path to the configuration file.

    Returns:
        Dict[str, Any]: Configuration dictionary.
    """
    config_file = Path(config_path)
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_file, 'r') as f:
        return json.load(f)

def _validate_config(config: Dict[str, Any]) -> None:
    """
    Validate the configuration dictionary.

    Args:
        config (Dict[str, Any]): Configuration to validate.

    Raises:
        ConfigurationError: If configuration is invalid.
    """
    validation_rules = {
        'timeout': lambda x: isinstance(x, (int, float)) and x > 0,
        'max_retries': lambda x: isinstance(x, int) and x >= 0,
        'base_url': lambda x: isinstance(x, str) and x.startswith('http')
    }

    for key, validator in validation_rules.items():
        if key in config and not validator(config[key]):
            raise ConfigurationError(f"Invalid configuration for {key}")