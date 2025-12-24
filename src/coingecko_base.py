import requests
from typing import Dict, Any, Optional
import logging

class CoinGeckoAPIError(Exception):
    """Custom exception for CoinGecko API errors."""
    pass

class CoinGeckoBaseMethod:
    """
    Base class for CoinGecko API interactions.
    
    Provides core functionality for making API requests with error handling.
    """
    BASE_URL = "https://api.coingecko.com/api/v3"
    
    def __init__(self, timeout: int = 10, max_retries: int = 3):
        """
        Initialize the CoinGecko Base Method.
        
        Args:
            timeout (int): Request timeout in seconds. Defaults to 10.
            max_retries (int): Maximum number of request retries. Defaults to 3.
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a GET request to the CoinGecko API.
        
        Args:
            endpoint (str): API endpoint to request.
            params (dict, optional): Query parameters for the request.
        
        Returns:
            dict: Parsed JSON response from the API.
        
        Raises:
            CoinGeckoAPIError: For API-related errors.
        """
        url = f"{self.BASE_URL}/{endpoint}"
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, params=params, timeout=self.timeout)
                
                # Raise an exception for HTTP errors
                response.raise_for_status()
                
                return response.json()
            
            except requests.exceptions.RequestException as e:
                self.logger.warning(f"Request attempt {attempt + 1} failed: {e}")
                
                if attempt == self.max_retries - 1:
                    self.logger.error(f"Max retries reached. Unable to complete request to {endpoint}")
                    raise CoinGeckoAPIError(f"Request failed after {self.max_retries} attempts: {e}")
        
        raise CoinGeckoAPIError("Unexpected error in request processing")