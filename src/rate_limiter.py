import time
import logging
from typing import Callable, Any, Optional
from functools import wraps

from .exceptions import RateLimitError, NetworkError

class RateLimiter:
    def __init__(self, max_calls: int = 10, period: float = 60.0, raise_on_limit: bool = True):
        """
        Initialize rate limiter with maximum calls per period.
        
        Args:
            max_calls (int): Maximum number of calls allowed in the given period.
            period (float): Time period in seconds.
            raise_on_limit (bool): Raise RateLimitError instead of waiting.
        """
        self.max_calls = max_calls
        self.period = period
        self.calls = []
        self.raise_on_limit = raise_on_limit

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            return self.call(func, *args, **kwargs)
        return wrapper

    def call(self, func: Callable, *args: Any, **kwargs: Any) -> Any:
        """
        Throttle function calls and manage rate limits.
        
        Args:
            func (Callable): Function to be rate limited.
        
        Returns:
            Result of the function call.
        
        Raises:
            RateLimitError: If rate limit is exceeded and raise_on_limit is True.
        """
        current_time = time.time()
        
        # Remove old call timestamps
        self.calls = [t for t in self.calls if current_time - t < self.period]
        
        if len(self.calls) >= self.max_calls:
            wait_time = self.period - (current_time - self.calls[0])
            logging.warning(f"Rate limit exceeded. Waiting {wait_time:.2f} seconds.")
            
            if self.raise_on_limit:
                raise RateLimitError(f"Rate limit of {self.max_calls} calls per {self.period} seconds exceeded")
            
            time.sleep(wait_time)
        
        try:
            result = func(*args, **kwargs)
            self.calls.append(current_time)
            return result
        except Exception as e:
            logging.error(f"Error during rate-limited call: {e}")
            raise

def retry(max_attempts: int = 3, 
          backoff_base: float = 2.0, 
          retriable_exceptions: Optional[tuple] = None) -> Callable:
    """
    Decorator for implementing retry logic with exponential backoff.
    
    Args:
        max_attempts (int): Maximum number of retry attempts.
        backoff_base (float): Base for exponential backoff calculation.
        retriable_exceptions (tuple): Exceptions that trigger retry.
    
    Returns:
        Decorated function with retry mechanism.
    """
    if retriable_exceptions is None:
        retriable_exceptions = (RateLimitError, NetworkError)

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except retriable_exceptions as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logging.error(f"Max retry attempts reached for {func.__name__}")
                        raise

                    wait_time = backoff_base ** attempts
                    logging.warning(
                        f"Retry attempt {attempts} for {func.__name__}. "
                        f"Waiting {wait_time:.2f} seconds. Error: {str(e)}"
                    )
                    time.sleep(wait_time)
        return wrapper
    return decorator