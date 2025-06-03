import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
import json

class ConfigurationError(Exception):
    """Exception raised for configuration-related errors."""
    pass

@dataclass
class CoinGeckoConfig:
    """Configuration handler for CoinGecko API client."""

    base_url: str = "https://api.coingecko.com/api/v3"
    api_key: Optional[str] = None
    timeout: int = 30
    rate_limit_delay: int = 1
    default_currency: str = "usd"
    additional_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Validate configuration after initialization."""
        self.validate_config()

    def validate_config(self):
        """Validate configuration parameters."""
        if not self.base_url:
            raise ConfigurationError("Base URL cannot be empty")
        
        if self.timeout <= 0:
            raise ConfigurationError("Timeout must be a positive integer")

    @classmethod
    def from_env(cls) -> 'CoinGeckoConfig':
        """
        Create configuration from environment variables.
        
        Environment variables:
        - COINGECKO_BASE_URL (optional)
        - COINGECKO_API_KEY (optional)
        - COINGECKO_TIMEOUT (optional)
        - COINGECKO_RATE_LIMIT_DELAY (optional)
        - COINGECKO_DEFAULT_CURRENCY (optional)
        """
        return cls(
            base_url=os.getenv('COINGECKO_BASE_URL', cls.base_url),
            api_key=os.getenv('COINGECKO_API_KEY'),
            timeout=int(os.getenv('COINGECKO_TIMEOUT', cls.timeout)),
            rate_limit_delay=int(os.getenv('COINGECKO_RATE_LIMIT_DELAY', cls.rate_limit_delay)),
            default_currency=os.getenv('COINGECKO_DEFAULT_CURRENCY', cls.default_currency)
        )

    @classmethod
    def from_file(cls, config_path: str) -> 'CoinGeckoConfig':
        """
        Create configuration from a JSON config file.
        
        Args:
            config_path (str): Path to the configuration JSON file
        
        Returns:
            CoinGeckoConfig: Configured instance
        
        Raises:
            ConfigurationError: If file cannot be read or parsed
        """
        try:
            with open(config_path, 'r') as config_file:
                config_data = json.load(config_file)
                return cls(**config_data)
        except FileNotFoundError:
            raise ConfigurationError(f"Configuration file not found: {config_path}")
        except json.JSONDecodeError:
            raise ConfigurationError(f"Invalid JSON in configuration file: {config_path}")

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to a dictionary.
        
        Returns:
            Dict[str, Any]: Configuration as a dictionary
        """
        return {
            'base_url': self.base_url,
            'api_key': self.api_key,
            'timeout': self.timeout,
            'rate_limit_delay': self.rate_limit_delay,
            'default_currency': self.default_currency,
            'additional_params': self.additional_params
        }