import os
from typing import Optional, Dict, Any, Union
from dotenv import load_dotenv

class ConfigurationError(Exception):
    """Exception raised for configuration-related errors."""
    pass

class CoinGeckoConfig:
    """
    Manages configuration for CoinGecko API integration.
    
    Supports configuration via:
    1. Programmatic configuration
    2. Environment variables
    3. Default configuration
    """
    
    DEFAULT_BASE_URL = 'https://api.coingecko.com/api/v3'
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 base_url: Optional[str] = None,
                 env_file: Optional[str] = None):
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
        load_dotenv(dotenv_path=env_file or '.env')
        
        # Validate base_url
        env_base_url = os.getenv('COINGECKO_BASE_URL')
        
        # Enforce base URL requirement
        if base_url is None and env_base_url is None:
            raise ValueError("base URL is required")
        
        # Choose base_url
        if base_url is not None:
            self.base_url = self._validate_base_url(base_url)
        elif env_base_url is not None:
            self.base_url = self._validate_base_url(env_base_url)
        else:
            self.base_url = self.DEFAULT_BASE_URL
        
        # Prioritize method order: 
        # 1. Programmatic configuration 
        # 2. Environment variables
        self.api_key = api_key or os.getenv('COINGECKO_API_KEY')
    
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
        
        # Protocol check
        if not base_url_str.startswith(('http://', 'https://')):
            raise ConfigurationError("Base URL must start with http:// or https://")
        
        return base_url_str
    
    def get_config(self) -> Dict[str, Any]:
        """
        Get a dictionary representation of the current configuration.
        
        Returns:
            Dict containing configuration parameters
        """
        return {
            "api_key": self.api_key,
            "base_url": self.base_url
        }