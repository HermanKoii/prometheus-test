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
    1. Environment variables
    2. .env file
    3. Programmatic configuration
    """
    
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
        """
        # Load environment variables from .env file if specified or default
        load_dotenv(dotenv_path=env_file or '.env')
        
        # Prioritize method order: 
        # 1. Programmatic configuration 
        # 2. Environment variables
        self.api_key = api_key or os.getenv('COINGECKO_API_KEY')
        
        # Use a specific method to validate base_url
        self.base_url = self._validate_base_url(base_url or os.getenv('COINGECKO_BASE_URL', 'https://api.coingecko.com/api/v3'))
    
    def _validate_base_url(self, base_url: Union[str, None, int]) -> str:
        """
        Validate and return a valid base URL.
        
        Args:
            base_url: URL to validate
        
        Returns:
            Validated base URL
        
        Raises:
            ConfigurationError: If base URL is invalid
        """
        # First check type
        if base_url is None or not isinstance(base_url, str):
            raise ConfigurationError("Base URL must be a non-empty string")
        
        # Then check content
        base_url = base_url.strip()
        if not base_url:
            raise ConfigurationError("Base URL must be a non-empty string")
        
        # Validate protocol
        if not base_url.startswith(('http://', 'https://')):
            raise ConfigurationError("Base URL must start with http:// or https://")
        
        return base_url
    
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