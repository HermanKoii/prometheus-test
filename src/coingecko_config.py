import os
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from pydantic import BaseModel, Field, ValidationError, validator

class CoinGeckoConfigError(Exception):
    """Base exception for CoinGecko configuration errors."""
    pass

class CoinGeckoConfigValidationError(CoinGeckoConfigError):
    """Raised when configuration fails validation."""
    pass

class CoinGeckoConfig(BaseModel):
    """
    Configuration class for CoinGecko API client.
    
    Validates and manages CoinGecko API configuration parameters.
    """
    base_url: str = Field(
        default="https://api.coingecko.com/api/v3", 
        description="Base URL for CoinGecko API"
    )
    api_key: Optional[str] = Field(
        default=None, 
        description="Optional API key for CoinGecko Pro"
    )
    timeout: int = Field(
        default=10, 
        gt=0, 
        le=60, 
        description="Timeout for API requests in seconds"
    )
    cache_enabled: bool = Field(
        default=True, 
        description="Enable response caching"
    )
    cache_ttl: int = Field(
        default=300, 
        gt=0, 
        description="Cache time-to-live in seconds"
    )

    @validator('base_url')
    def validate_base_url(cls, v):
        """
        Validate base URL format.
        
        Args:
            v (str): Base URL to validate
        
        Raises:
            CoinGeckoConfigValidationError: If URL is invalid
        """
        if not v.startswith(('http://', 'https://')):
            raise CoinGeckoConfigValidationError(f"Invalid base URL: {v}")
        return v

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dict[str, Any]: Configuration as a dictionary
        """
        return self.dict()

    @classmethod
    def from_env(cls) -> 'CoinGeckoConfig':
        """
        Create configuration from environment variables.
        
        Returns:
            CoinGeckoConfig: Configuration instance
        """
        config_dict = {
            'base_url': os.getenv('COINGECKO_BASE_URL', 'https://api.coingecko.com/api/v3'),
            'api_key': os.getenv('COINGECKO_API_KEY'),
            'timeout': int(os.getenv('COINGECKO_TIMEOUT', 10)),
            'cache_enabled': os.getenv('COINGECKO_CACHE_ENABLED', 'true').lower() == 'true',
            'cache_ttl': int(os.getenv('COINGECKO_CACHE_TTL', 300))
        }
        
        try:
            return cls(**config_dict)
        except ValidationError as e:
            raise CoinGeckoConfigValidationError(f"Configuration validation failed: {e}")