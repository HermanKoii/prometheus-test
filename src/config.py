import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class ConfigurationError(Exception):
    """Custom exception for configuration loading errors."""
    pass

class CoinGeckoConfig:
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize CoinGecko API configuration.
        
        Args:
            config_file (Optional[str]): Path to a custom configuration file.
        """
        self._config: Dict[str, Any] = {}
        self._load_configuration(config_file)

    def _load_configuration(self, config_file: Optional[str] = None):
        """
        Load configuration from multiple sources with precedence:
        1. Environment variables
        2. Specified config file
        3. Default settings
        
        Args:
            config_file (Optional[str]): Path to a custom configuration file.
        """
        # Load .env file if exists
        load_dotenv(config_file or '.env')

        # Default configuration with sane defaults
        default_config = {
            'api_base_url': 'https://api.coingecko.com/api/v3',
            'api_timeout': 10,
            'max_retries': 3,
            'cache_duration': 300  # 5 minutes
        }

        # Override with environment variables
        for key, default_value in default_config.items():
            env_key = f'COINGECKO_{key.upper()}'
            value = os.getenv(env_key, default_value)

            # Type conversion
            if isinstance(default_value, int):
                try:
                    value = int(value)
                except ValueError:
                    raise ConfigurationError(f"Invalid configuration value for {env_key}")
            
            self._config[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a configuration value.
        
        Args:
            key (str): Configuration key to retrieve
            default (Any, optional): Default value if key not found
        
        Returns:
            Any: Configuration value
        """
        return self._config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """
        Allow dictionary-like access to configuration.
        
        Args:
            key (str): Configuration key
        
        Returns:
            Any: Configuration value
        
        Raises:
            KeyError: If configuration key is not found
        """
        if key not in self._config:
            raise KeyError(f"Configuration key '{key}' not found")
        return self._config[key]