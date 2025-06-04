"""
Historical Price Retrieval Service with Comprehensive Error Handling.

This module provides robust error handling for retrieving historical 
cryptocurrency price data from the CoinGecko API.
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import requests

from .exceptions import (
    HistoricalPriceRetrievalError,
    RateLimitError,
    DataNotFoundError,
    NetworkError
)

class HistoricalPriceService:
    """
    Service for retrieving and handling historical cryptocurrency prices.
    
    Implements comprehensive error handling and validation for historical price data.
    """
    
    def __init__(self, base_url: str = "https://api.coingecko.com/api/v3"):
        """
        Initialize the historical price service.
        
        Args:
            base_url (str): Base URL for CoinGecko API
        """
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
    
    def get_historical_price(
        self, 
        coin_id: str, 
        date: str,
        currency: str = 'usd'
    ) -> Optional[float]:
        """
        Retrieve historical price for a specific coin and date.
        
        Args:
            coin_id (str): Unique identifier for the cryptocurrency
            date (str): Date in 'dd-mm-yyyy' format
            currency (str, optional): Target currency for price. Defaults to 'usd'.
        
        Returns:
            Optional[float]: Historical price if available, None otherwise
        
        Raises:
            HistoricalPriceRetrievalError: For various retrieval issues
        """
        self.logger.info(f"Fetching historical price for {coin_id} on {date}")
        
        try:
            # Validate inputs
            self._validate_inputs(coin_id, date, currency)
            
            # Construct API request URL
            url = f"{self.base_url}/coins/{coin_id}/history"
            params = {
                'date': date,
                'localization': 'false'
            }
            
            # Make API request with robust error handling
            response = self._make_request(url, params)
            
            # Extract and return price
            return self._extract_price(response, currency)
        
        except requests.exceptions.RequestException as e:
            # Handle network-related errors
            error_msg = f"Network error retrieving price: {str(e)}"
            self.logger.error(error_msg)
            raise NetworkError(error_msg, coin_id=coin_id, date=date) from e
        
        except ValueError as e:
            # Handle input validation errors
            self.logger.error(str(e))
            raise HistoricalPriceRetrievalError(str(e), coin_id=coin_id, date=date)
    
    def _validate_inputs(self, coin_id: str, date: str, currency: str):
        """
        Validate input parameters for historical price retrieval.
        
        Args:
            coin_id (str): Cryptocurrency identifier
            date (str): Date string
            currency (str): Target currency
        
        Raises:
            ValueError: If inputs are invalid
        """
        if not coin_id or not isinstance(coin_id, str):
            raise ValueError("Invalid coin ID")
        
        if not date or not self._is_valid_date_format(date):
            raise ValueError(f"Invalid date format: {date}. Use dd-mm-yyyy.")
        
        if not currency or not isinstance(currency, str):
            raise ValueError("Invalid currency")
    
    def _is_valid_date_format(self, date_str: str) -> bool:
        """
        Check if date string matches dd-mm-yyyy format.
        
        Args:
            date_str (str): Date string to validate
        
        Returns:
            bool: Whether date is in valid format
        """
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
            return True
        except ValueError:
            return False
    
    def _make_request(self, url: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make API request with error handling.
        
        Args:
            url (str): API endpoint URL
            params (Dict): Request parameters
        
        Returns:
            Dict[str, Any]: API response
        
        Raises:
            RateLimitError: If rate limit is exceeded
            DataNotFoundError: If requested data is not found
            HistoricalPriceRetrievalError: For other API errors
        """
        try:
            response = requests.get(url, params=params, timeout=10)
            
            # Handle different HTTP status codes
            if response.status_code == 429:
                raise RateLimitError("API rate limit exceeded")
            
            if response.status_code == 404:
                raise DataNotFoundError("Historical price data not found")
            
            response.raise_for_status()  # Raise exception for other bad status codes
            
            return response.json()
        
        except requests.exceptions.Timeout:
            raise NetworkError("Request timed out")
    
    def _extract_price(self, response: Dict[str, Any], currency: str) -> Optional[float]:
        """
        Extract price from API response.
        
        Args:
            response (Dict): API response
            currency (str): Target currency
        
        Returns:
            Optional[float]: Extracted price
        
        Raises:
            DataNotFoundError: If price cannot be extracted
        """
        try:
            market_data = response.get('market_data', {})
            current_prices = market_data.get('current_price', {})
            
            price = current_prices.get(currency.lower())
            
            if price is None:
                raise DataNotFoundError(f"Price not found for currency: {currency}")
            
            return float(price)
        
        except (KeyError, TypeError, ValueError) as e:
            raise DataNotFoundError(f"Failed to extract price: {str(e)}")