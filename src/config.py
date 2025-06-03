from typing import Optional
from dotenv import load_dotenv
import os

class CoinGeckoConfig:
    """
    Configuration class for managing CoinGecko API credentials and settings.
    
    Supports configuration via environment variables and optional direct parameter setting.
    Provides secure and flexible API configuration management.
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        base_url: Optional[str] = None,
        timeout: int = 10,
        retries: int = 3
    ):
        """
        Initialize CoinGecko API configuration.
        
        Args:
            api_key (Optional[str]): CoinGecko API key. Defaults to environment variable.
            base_url (Optional[str]): Base URL for CoinGecko API. Optional.
            timeout (int): HTTP request timeout in seconds. Defaults to 10.
            retries (int): Number of retry attempts for failed requests. Defaults to 3.
        """
        # Load environment variables from .env file
        load_dotenv()
        
        # Prioritize passed parameters, then environment variables
        self.api_key = api_key or os.getenv('COINGECKO_API_KEY')
        self.base_url = base_url or os.getenv('COINGECKO_BASE_URL', 'https://api.coingecko.com/api/v3')
        
        self.timeout = max(1, timeout)  # Minimum timeout of 1 second
        self.retries = max(0, retries)  # Non-negative retries
        
        self._validate_config()
    
    def _validate_config(self):
        """
        Validate configuration parameters and raise exceptions for invalid settings.
        """
        if not self.base_url:
            raise ValueError("CoinGecko base URL must be provided")
        
        if not self.base_url.startswith(('http://', 'https://')):
            raise ValueError("Base URL must start with http:// or https://")
    
    def get_api_credentials(self) -> dict:
        """
        Retrieve API credentials securely.
        
        Returns:
            dict: A dictionary containing API configuration parameters.
        """
        return {
            'api_key': self.api_key,
            'base_url': self.base_url,
            'timeout': self.timeout,
            'retries': self.retries
        }
    
    def is_valid(self) -> bool:
        """
        Check if the current configuration is valid.
        
        Returns:
            bool: True if configuration is valid, False otherwise.
        """
        try:
            self._validate_config()
            return True
        except ValueError:
            return False