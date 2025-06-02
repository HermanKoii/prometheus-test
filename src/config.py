import os
import math
from typing import Dict, Any, Optional, Union
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
        timeout: Optional[Union[int, float, str]] = None
    ):
        """
        Initialize configuration with optional overrides.

        Args:
            base_url: Override for CoinGecko API base URL
            api_key: Override for CoinGecko API key
            timeout: Override for API request timeout
        
        Raises:
            ConfigurationError: If timeout is not a valid integer
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

        # Configure timeout with robust validation
        self.timeout = self._validate_timeout(timeout)

    def _validate_timeout(self, timeout: Optional[Union[int, float, str]]) -> int:
        """
        Validate and convert timeout to integer.

        Args:
            timeout: Timeout value to validate

        Returns:
            Validated timeout as integer

        Raises:
            ConfigurationError: If timeout is invalid
        """
        # If no timeout provided, use default from environment or static default
        if timeout is None:
            timeout = os.getenv('COINGECKO_API_TIMEOUT', 10)

        # Convert to string to handle different input types safely
        timeout_str = str(timeout).strip()

        # Check for empty or blank strings
        if not timeout_str:
            raise ConfigurationError("Invalid timeout value. Must be a valid positive number.")

        try:
            # Try converting to float
            timeout_value = float(timeout_str)
            
            # Additional checks
            if (
                not isinstance(timeout_value, (int, float)) or  # Not a number
                math.isnan(timeout_value) or  # Not a number (NaN)
                math.isinf(timeout_value) or  # Infinity
                timeout_value <= 0  # Non-positive number
            ):
                raise ValueError("Invalid timeout")
            
            return int(timeout_value)
        except (ValueError, TypeError):
            raise ConfigurationError("Invalid timeout value. Must be a valid positive number.")

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