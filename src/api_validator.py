import requests
import logging
from typing import Dict, Any, Optional

class CoinGeckoAPIConnectionError(Exception):
    """Custom exception for CoinGecko API connection errors."""
    pass

class CoinGeckoAPIValidator:
    """
    A validator class for checking CoinGecko API connectivity and health.
    
    This class provides methods to validate API connection and retrieve basic 
    system health information.
    """
    
    def __init__(self, base_url: str = "https://api.coingecko.com/api/v3"):
        """
        Initialize the CoinGecko API validator.
        
        Args:
            base_url (str, optional): Base URL for the CoinGecko API. 
                                      Defaults to the official endpoint.
        """
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
    
    def validate_connection(self, timeout: int = 10) -> Dict[str, Any]:
        """
        Validate the CoinGecko API connection by performing a health check.
        
        Args:
            timeout (int, optional): Request timeout in seconds. Defaults to 10.
        
        Returns:
            Dict[str, Any]: Connection health information.
        
        Raises:
            CoinGeckoAPIConnectionError: If connection validation fails.
        """
        try:
            response = requests.get(
                f"{self.base_url}/ping", 
                timeout=timeout
            )
            
            # Check response status and content
            if response.status_code != 200:
                raise CoinGeckoAPIConnectionError(
                    f"API Connection failed. Status code: {response.status_code}"
                )
            
            result = response.json()
            
            # Validate expected response structure
            if result.get('gecko_says') != '(V3) To the Moon!':
                raise CoinGeckoAPIConnectionError(
                    "Unexpected API response format"
                )
            
            self.logger.info("CoinGecko API connection validated successfully")
            return result
        
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Network error during API connection: {e}")
            raise CoinGeckoAPIConnectionError(f"Network error: {e}") from e
        
        except ValueError as e:
            self.logger.error(f"JSON parsing error: {e}")
            raise CoinGeckoAPIConnectionError(f"Invalid JSON response: {e}") from e