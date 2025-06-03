import time
import pytest
from src.rate_limiter import RateLimiter, retry
from src.exceptions import RateLimitError, NetworkError

def test_rate_limiter_basic():
    """Test basic rate limiter functionality."""
    limiter = RateLimiter(max_calls=2, period=1.0, raise_on_limit=True)
    
    @limiter
    def dummy_func():
        return True
    
    # First two calls should succeed
    assert dummy_func() is True
    assert dummy_func() is True
    
    # Third call should trigger rate limit
    with pytest.raises(RateLimitError):
        dummy_func()

def test_rate_limiter_wait_mode():
    """Test rate limiter in wait mode."""
    limiter = RateLimiter(max_calls=2, period=1.0, raise_on_limit=False)
    
    @limiter
    def dummy_func():
        return True
    
    start_time = time.time()
    assert dummy_func() is True
    assert dummy_func() is True
    assert dummy_func() is True
    
    # Ensure some waiting occurred
    assert time.time() - start_time > 1.0

def test_retry_decorator():
    """Test retry decorator with mock failures."""
    attempts = 0
    
    @retry(max_attempts=3)
    def flaky_function():
        nonlocal attempts
        attempts += 1
        if attempts < 3:
            raise NetworkError("Temporary network issue")
        return True
    
    result = flaky_function()
    assert result is True
    assert attempts == 3

def test_retry_max_attempts():
    """Test retry decorator reaches max attempts."""
    attempts = 0
    
    @retry(max_attempts=2)
    def always_fail():
        nonlocal attempts
        attempts += 1
        raise RateLimitError("Rate limit exceeded")
    
    with pytest.raises(RateLimitError):
        always_fail()
    
    assert attempts == 2

def test_retry_different_exceptions():
    """Test retry with custom exception types."""
    attempts = 0
    
    @retry(max_attempts=3, retriable_exceptions=(ValueError, TypeError))
    def selective_retry():
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise ValueError("First attempt")
        if attempts == 2:
            raise TypeError("Second attempt")
        return True
    
    result = selective_retry()
    assert result is True
    assert attempts == 3