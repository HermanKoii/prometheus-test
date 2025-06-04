"""
Custom exceptions for CoinGecko API interactions.

This module defines specific exceptions to handle various error scenarios
during historical price data retrieval.
"""

class CoinGeckoAPIError(Exception):
    """Base exception for CoinGecko API-related errors."""
    pass

class HistoricalPriceRetrievalError(CoinGeckoAPIError):
    """
    Raised when there's an error retrieving historical price data.

    Attributes:
        message (str): Detailed error description
        status_code (int, optional): HTTP status code of the error
        coin_id (str, optional): ID of the coin for which retrieval failed
        date (str, optional): Date for which price retrieval failed
    """
    def __init__(self, message: str, status_code: int = None, 
                 coin_id: str = None, date: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.coin_id = coin_id
        self.date = date

class RateLimitError(HistoricalPriceRetrievalError):
    """
    Raised when API rate limit is exceeded.
    
    Indicates that too many requests have been made in a short period.
    """
    pass

class DataNotFoundError(HistoricalPriceRetrievalError):
    """
    Raised when requested historical price data is not available.
    
    This could occur due to missing data for a specific coin or date.
    """
    pass

class NetworkError(HistoricalPriceRetrievalError):
    """
    Raised for network-related issues during API request.
    
    Includes connection timeouts, DNS failures, etc.
    """
    pass