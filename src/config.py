"""
Module for managing CoinGecko API configuration via environment variables.

This module provides secure loading and validation of CoinGecko API credentials
from environment variables, with comprehensive error handling.
"""

import os
from typing import Optional
from dotenv import load_dotenv

class ConfigurationError(Exception):
    """Raised when there's an issue with configuration loading or validation."""
    pass

def load_config() -> dict:
    """
    Load CoinGecko API configuration from environment variables.

    Loads variables from .env file if present, validates required credentials,
    and returns a configuration dictionary.

    Returns:
        dict: Configuration dictionary with API credentials.

    Raises:
        ConfigurationError: If required environment variables are missing or invalid.
    """
    # Load environment variables from .env file if it exists
    load_dotenv()

    # Retrieve API configuration
    api_key = os.getenv('COINGECKO_API_KEY')
    base_url = os.getenv('COINGECKO_API_BASE_URL', 'https://api.coingecko.com/api/v3')

    # Validate configuration
    if not api_key:
        raise ConfigurationError(
            "COINGECKO_API_KEY is required. "
            "Please set it in your .env file or environment variables."
        )

    # Validate base URL format (basic validation)
    if not base_url.startswith(('http://', 'https://')):
        raise ConfigurationError(f"Invalid base URL: {base_url}")

    return {
        'api_key': api_key,
        'base_url': base_url
    }

def get_config_value(key: str, default: Optional[str] = None) -> Optional[str]:
    """
    Safely retrieve a configuration value from environment variables.

    Args:
        key (str): Environment variable name.
        default (Optional[str], optional): Default value if key is not found.

    Returns:
        Optional[str]: Configuration value or default.
    """
    return os.getenv(key, default)