import logging
from typing import Optional

class CoinGeckoAPIError(Exception):
    """Base exception for CoinGecko API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None):
        self.message = message
        self.status_code = status_code
        logging.error(f"CoinGecko API Error: {message} (Status Code: {status_code})")
        super().__init__(self.message)

class RateLimitError(CoinGeckoAPIError):
    """Raised when API rate limit is exceeded."""
    def __init__(self, message: str = "API rate limit exceeded", retry_after: Optional[int] = None):
        super().__init__(message)
        self.retry_after = retry_after

class AuthenticationError(CoinGeckoAPIError):
    """Raised when there are authentication issues."""
    pass

class NetworkError(CoinGeckoAPIError):
    """Raised for network-related issues."""
    pass

class ValidationError(CoinGeckoAPIError):
    """Raised for input validation errors."""
    pass