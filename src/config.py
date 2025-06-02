import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

class ConfigurationError(Exception):
    """Custom exception for configuration loading errors."""
    pass

class CoinGeckoConfig:
    """
    Configuration loader for CoinGecko API client.

    Supports configuration from multiple sources:
    1. Environment variables
    2. .env file
    3. Default configuration
    """

    def __init__(
        self, 
        base_url: Optional[str] = None, 
        api_key: Optional[str] = None,
        timeout: Optional[int] = None
    ):
        """
        Initialize configuration with optional overrides.

        Args:
            base_url: Override for CoinGecko API base URL
            api_key: Override for CoinGecko API key
            timeout: Override for API request timeout
        """
        # Load .env file first (if exists)
        load_dotenv()

        # Configure base URL
        self.base_url = base_url or os.getenv(
            'COINGECKO_BASE_URL', 
            'https://api.coingecko.com/api/v3'
        )

        # Configure API key (optional)
        self.api_key = api_key or os.getenv('COINGECKO_API_KEY')

        # Configure timeout
        try:
            self.timeout = timeout or int(os.getenv('COINGECKO_API_TIMEOUT', 10))
        except ValueError:
            raise ConfigurationError("Invalid timeout value. Must be an integer.")

    def get_config(self) -> Dict[str, Any]:
        """
        Retrieve complete configuration as a dictionary.

        Returns:
            Dictionary containing configuration parameters
        """
        return {
            'base_url': self.base_url,
            'api_key': '***' if self.api_key else None,  # Mask API key
            'timeout': self.timeout
        }

    @classmethod
    def from_dict(cls, config: Dict[str, Any]) -> 'CoinGeckoConfig':
        """
        Create configuration from a dictionary.

        Args:
            config: Dictionary with configuration parameters

        Returns:
            CoinGeckoConfig instance
        """
        return cls(
            base_url=config.get('base_url'),
            api_key=config.get('api_key'),
            timeout=config.get('timeout')
        )