import os
from typing import Optional, Dict, Any
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
        self.base_url = base_url or os.getenv('COINGECKO_BASE_URL', 'https://api.coingecko.com/api/v3')
        
        # Validate configuration
        self._validate_config()
    
    def _validate_config(self):
        """
        Validate configuration parameters.
        
        Raises:
            ConfigurationError: If required parameters are missing or invalid
        """
        errors = []
        
        if not self.base_url:
            errors.append("Base URL is required")
        
        # Optional: Add more specific validation for base_url format
        if not isinstance(self.base_url, str):
            errors.append("Base URL must be a string")
        
        # API key is optional but can be validated if present
        if self.api_key and not isinstance(self.api_key, str):
            errors.append("API Key must be a string")
        
        if errors:
            raise ConfigurationError("\n".join(errors))
    
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