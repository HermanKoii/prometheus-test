import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import json

class ConfigurationError(Exception):
    """Custom exception for configuration-related errors."""
    pass

class CoinGeckoConfig:
    """
    Configuration class for CoinGecko API client.
    Loads configuration from environment variables, .env file, or config file.
    
    Supports multiple sources with precedence:
    1. Explicitly passed parameters
    2. Environment variables
    3. .env file
    4. Configuration file
    5. Default values
    """
    
    DEFAULT_CONFIG_FILE = 'config.json'
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        base_url: Optional[str] = None, 
        timeout: Optional[int] = None,
        config_file: Optional[str] = None
    ):
        """
        Initialize CoinGecko configuration.
        
        Args:
            api_key (Optional[str]): API key for CoinGecko.
            base_url (Optional[str]): Base URL for CoinGecko API.
            timeout (Optional[int]): Request timeout in seconds.
            config_file (Optional[str]): Path to custom configuration file.
        """
        # Load .env file first
        load_dotenv()
        
        # Load configuration
        self.config = self._load_configuration(
            api_key, base_url, timeout, config_file
        )
    
    def _load_configuration(
        self, 
        api_key: Optional[str], 
        base_url: Optional[str], 
        timeout: Optional[int],
        config_file: Optional[str]
    ) -> Dict[str, Any]:
        """
        Load configuration from multiple sources with precedence.
        
        Args:
            api_key, base_url, timeout: Explicitly passed parameters
            config_file: Custom configuration file path
        
        Returns:
            Dict[str, Any]: Loaded configuration
        """
        config = {
            'api_key': os.getenv('COINGECKO_API_KEY'),
            'base_url': os.getenv('COINGECKO_BASE_URL', 'https://api.coingecko.com/api/v3'),
            'timeout': int(os.getenv('COINGECKO_TIMEOUT', 30))
        }
        
        # Try loading from configuration file
        if config_file or os.path.exists(self.DEFAULT_CONFIG_FILE):
            try:
                config_path = config_file or self.DEFAULT_CONFIG_FILE
                with open(config_path, 'r') as f:
                    file_config = json.load(f)
                config.update(file_config)
            except (FileNotFoundError, json.JSONDecodeError) as e:
                raise ConfigurationError(f"Error reading config file: {e}")
        
        # Override with explicitly passed parameters
        if api_key is not None:
            config['api_key'] = api_key
        if base_url is not None:
            config['base_url'] = base_url
        if timeout is not None:
            config['timeout'] = timeout
        
        # Validate configuration
        self._validate_configuration(config)
        
        return config
    
    def _validate_configuration(self, config: Dict[str, Any]):
        """
        Validate the configuration parameters.
        
        Args:
            config (Dict[str, Any]): Configuration to validate
        
        Raises:
            ConfigurationError: If configuration is invalid
        """
        if not config.get('base_url'):
            raise ConfigurationError("Base URL is required")
        
        try:
            timeout = int(config.get('timeout', 30))
            if timeout <= 0:
                raise ValueError("Timeout must be a positive integer")
        except ValueError:
            raise ConfigurationError("Invalid timeout value")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            key (str): Configuration key
            default (Any, optional): Default value if key not found
        
        Returns:
            Any: Configuration value
        """
        return self.config.get(key, default)
    
    def __getitem__(self, key: str) -> Any:
        """
        Allow dictionary-style access to configuration.
        
        Args:
            key (str): Configuration key
        
        Returns:
            Any: Configuration value
        
        Raises:
            KeyError: If key is not found
        """
        return self.config[key]