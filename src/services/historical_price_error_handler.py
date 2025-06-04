import logging
import time
import requests
from typing import Callable, Any

from src.exceptions.historical_price_exceptions import (
    NetworkError, 
    RateLimitError, 
    DataNotFoundError, 
    InvalidParameterError
)

class HistoricalPriceErrorHandler:
    """
    Provides error handling and retry mechanisms for historical price retrieval.
    
    Handles common error scenarios like network issues, rate limits, and data retrieval problems.
    """
    
    @staticmethod
    def handle_error(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Decorator to handle errors in historical price retrieval methods.
        
        Args:
            func (Callable): The method to be decorated with error handling.
        
        Returns:
            Callable: Wrapped method with error handling logic.
        
        Raises:
            NetworkError: When network connectivity issues occur
            RateLimitError: When API rate limit is exceeded
            DataNotFoundError: When requested data is unavailable
            InvalidParameterError: When invalid parameters are provided
        """
        def wrapper(*args, **kwargs):
            max_retries = kwargs.pop('max_retries', 3)
            retry_delay = kwargs.pop('retry_delay', 1)
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                
                except requests.exceptions.ConnectionError as e:
                    logging.error(f"Network error on attempt {attempt + 1}: {e}")
                    if attempt == max_retries - 1:
                        raise NetworkError(str(e))
                
                except requests.exceptions.HTTPError as e:
                    status_code = e.response.status_code
                    
                    if status_code == 429:  # Too Many Requests
                        retry_after = int(e.response.headers.get('Retry-After', retry_delay))
                        logging.warning(f"Rate limit exceeded. Retrying in {retry_after} seconds.")
                        time.sleep(retry_after)
                        continue
                    
                    if status_code == 404:
                        raise DataNotFoundError()
                    
                    if status_code == 400:
                        raise InvalidParameterError(message=str(e))
                
                except Exception as e:
                    logging.error(f"Unexpected error: {e}")
                    raise
                
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
            
            raise Exception("Max retries exceeded")
        
        return wrapper