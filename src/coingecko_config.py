import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv

class CoinGeckoConfig:
    """
    Configuration class for CoinGecko API client.
    
    Manages API configuration parameters with support for environment variables and default values.
    """
    
    def __init__(self, 
                 api_key: Optional[str] = None, 
                 base_url: Optional[str] = None, 
                 default_currency: str = 'usd',
                 timeout: int = 10):
        """
        Initialize CoinGecko API configuration.
        
        Args:
            api_key (Optional[str]): CoinGecko API key. Defaults to environment variable.
            base_url (Optional[str]): Base URL for CoinGecko API. Defaults to environment variable.
            default_currency (str): Default currency for price conversions. Defaults to 'usd'.
            timeout (int): Request timeout in seconds. Defaults to 10 seconds.
        """
        # Load environment variables from .env file
        load_dotenv()
        
        # Prioritize passed parameters, then environment variables, then default values
        self._api_key = api_key or os.getenv('COINGECKO_API_KEY')
        self._base_url = base_url or os.getenv('COINGECKO_BASE_URL', 'https://api.coingecko.com/api/v3')
        self._default_currency = default_currency
        self._timeout = timeout
    
    @property
    def api_key(self) -> Optional[str]:
        """Get the configured API key."""
        return self._api_key
    
    @property
    def base_url(self) -> str:
        """Get the base URL for the CoinGecko API."""
        return self._base_url
    
    @property
    def default_currency(self) -> str:
        """Get the default currency for price conversions."""
        return self._default_currency
    
    @property
    def timeout(self) -> int:
        """Get the request timeout in seconds."""
        return self._timeout
    
    def get_config(self) -> Dict[str, Any]:
        """
        Retrieve the current configuration as a dictionary.
        
        Returns:
            Dict[str, Any]: Configuration parameters
        """
        return {
            'api_key': self._api_key,
            'base_url': self._base_url,
            'default_currency': self._default_currency,
            'timeout': self._timeout
        }
    
    def validate(self) -> bool:
        """
        Validate the current configuration.
        
        Returns:
            bool: True if configuration is valid, False otherwise
        """
        return bool(self._base_url) and self._timeout > 0