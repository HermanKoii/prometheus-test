import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

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
        Initialize CoinGecko API configuration.
        
        :param api_key: Optional API key for CoinGecko
        :param base_url: Optional base URL for CoinGecko API
        :param env_file: Path to .env file (default: '.env')
        """
        # Load environment variables from .env file if it exists
        if env_file:
            load_dotenv(dotenv_path=env_file)
        
        # Prioritize constructor arguments, then environment variables
        self.api_key = api_key or os.getenv('COINGECKO_API_KEY')
        self.base_url = base_url or os.getenv('COINGECKO_BASE_URL', 'https://api.coingecko.com/api/v3')
        
        # Additional configurable parameters
        self.request_timeout = int(os.getenv('COINGECKO_REQUEST_TIMEOUT', 10))
        self.retries = int(os.getenv('COINGECKO_RETRIES', 3))
        
        # Validate critical configuration
        self._validate_config()
    
    def _validate_config(self):
        """
        Validate critical configuration parameters.
        
        Raises:
            ValueError: If critical configuration is missing
        """
        errors = []
        
        if not self.base_url:
            errors.append("CoinGecko base URL is required")
        
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to a dictionary.
        
        :return: Dictionary representation of configuration
        """
        return {
            'api_key': self.api_key,
            'base_url': self.base_url,
            'request_timeout': self.request_timeout,
            'retries': self.retries
        }