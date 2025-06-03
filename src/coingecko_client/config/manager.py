"""
Configuration management for the CoinGecko API client.

Handles loading, validating, and managing configuration 
parameters from various sources.
"""

import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

from .exceptions import (
    MissingConfigurationError, 
    InvalidConfigurationError, 
    ConfigurationLoadError
)
from .logging_config import get_logger

class ConfigurationManager:
    """
    Manages configuration for the CoinGecko API client.

    Supports loading configuration from environment variables, 
    .env files, and direct parameter passing.
    """

    def __init__(
        self, 
        env_file: Optional[str] = None, 
        override_config: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the configuration manager.

        Args:
            env_file (Optional[str], optional): Path to .env file. Defaults to None.
            override_config (Optional[Dict[str, Any]], optional): Configuration overrides. Defaults to None.
        """
        self._logger = get_logger('config_manager')
        self._config: Dict[str, Any] = {}
        
        # Load environment variables
        if env_file:
            try:
                load_dotenv(env_file)
            except Exception as e:
                raise ConfigurationLoadError(f"Environment file {env_file}", e)

        # Load configurations
        self._load_config(override_config or {})

    def _load_config(self, override_config: Dict[str, Any]):
        """
        Load configuration from different sources.

        Args:
            override_config (Dict[str, Any]): Configuration overrides
        """
        # Default configuration
        default_config = {
            'base_url': os.getenv('COINGECKO_BASE_URL', 'https://api.coingecko.com/api/v3'),
            'api_key': os.getenv('COINGECKO_API_KEY'),
            'timeout': float(os.getenv('COINGECKO_TIMEOUT', 10)),
            'max_retries': int(os.getenv('COINGECKO_MAX_RETRIES', 3))
        }

        # Merge configurations with precedence: override_config > environment > defaults
        self._config = {**default_config, **{k: v for k, v in override_config.items() if v is not None}}

        # Validate configuration
        self._validate_config()

    def _validate_config(self):
        """
        Validate configuration parameters.

        Raises:
            InvalidConfigurationError: If configuration is invalid
        """
        # Validate base URL
        if not self._config.get('base_url') or self._config.get('base_url') == '':
            raise MissingConfigurationError('base_url')

        # Validate timeout
        try:
            timeout = float(self._config.get('timeout', 10))
            if timeout <= 0:
                raise ValueError("Timeout must be positive")
        except ValueError:
            raise InvalidConfigurationError("Invalid timeout value", 'timeout')

        # Log configuration (excluding sensitive information)
        safe_config = {k: v for k, v in self._config.items() if k != 'api_key'}
        self._logger.info(f"Configuration loaded: {safe_config}")

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.

        Args:
            key (str): Configuration key
            default (Any, optional): Default value if key not found. Defaults to None.

        Returns:
            Any: Configuration value
        """
        return self._config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """
        Get a configuration value using dictionary-style access.

        Args:
            key (str): Configuration key

        Returns:
            Any: Configuration value

        Raises:
            KeyError: If key is not found
        """
        if key not in self._config:
            raise KeyError(f"Configuration key '{key}' not found")
        return self._config[key]