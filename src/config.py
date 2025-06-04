import os
from typing import Dict, Any, Optional, Union
from dotenv import load_dotenv

class ConfigurationError(Exception):
    """Custom exception for configuration errors."""
    pass

class CoinGeckoConfig:
    """
    Configuration management for CoinGecko API integration.
    
    Supports loading configuration from:
    1. Environment variables
    2. .env files
    3. Programmatic configuration
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        base_url: Optional[str] = None, 
        env_file: Optional[str] = '.env'
    ):
        """
        Initialize CoinGecko configuration.

        Args:
            api_key: Optional API key for CoinGecko
            base_url: Optional base URL for API requests
            env_file: Optional path to .env file (defaults to .env in project root)

        Raises:
            ValueError: If no base URL is provided
        """
        # Load environment variables from .env file if specified or default
        if env_file:
            load_dotenv(dotenv_path=env_file)
        
        # Validate base_url
        env_base_url = os.getenv('COINGECKO_BASE_URL')
        
        # Set base URL with precedence: constructor > env > default
        if base_url is None:
            base_url = env_base_url or 'https://api.coingecko.com/api/v3'
        
        # Validate and set base URL
        self.base_url = self._validate_base_url(base_url)
        
        # Set API key from constructor or environment
        self.api_key = api_key or os.getenv('COINGECKO_API_KEY')
        
        # Set timeout and retries from environment or default
        self.request_timeout = int(os.getenv('COINGECKO_REQUEST_TIMEOUT', 10))
        self.retries = int(os.getenv('COINGECKO_RETRIES', 3))
    
    def _validate_base_url(self, base_url: Optional[Union[str, int]]) -> str:
        """
        Validate and return a valid base URL.

        Args:
            base_url: URL to validate

        Returns:
            Validated base URL

        Raises:
            ConfigurationError: If base URL is invalid
        """
        # Explicit type and None check
        if base_url is None:
            raise ConfigurationError("Base URL must be a non-empty string")
        
        # Convert to string
        try:
            base_url_str = str(base_url)
        except Exception:
            raise ConfigurationError("Base URL must be a non-empty string")
        
        # Strip whitespace
        base_url_str = base_url_str.strip()
        
        # Empty string check
        if not base_url_str:
            raise ConfigurationError("Base URL must be a non-empty string")
        
        return base_url_str
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to a dictionary.

        Returns:
            Dictionary representation of configuration
        """
        return {
            'api_key': self.api_key,
            'base_url': self.base_url,
            'request_timeout': self.request_timeout,
            'retries': self.retries
        }