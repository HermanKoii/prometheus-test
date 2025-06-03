import pytest
import logging
from src.exceptions import (
    CoinGeckoAPIError, 
    RateLimitError, 
    AuthenticationError, 
    NetworkError, 
    ValidationError
)

def test_base_exception():
    """Test base CoinGeckoAPIError functionality."""
    with pytest.raises(CoinGeckoAPIError) as exc_info:
        raise CoinGeckoAPIError("Test error", status_code=400)
    
    assert str(exc_info.value) == "Test error"
    assert exc_info.value.status_code == 400

def test_rate_limit_error():
    """Test RateLimitError with retry information."""
    error = RateLimitError(retry_after=60)
    
    assert isinstance(error, CoinGeckoAPIError)
    assert error.retry_after == 60
    assert str(error) == "API rate limit exceeded"

def test_authentication_error():
    """Test AuthenticationError specific behavior."""
    with pytest.raises(AuthenticationError) as exc_info:
        raise AuthenticationError("Invalid API key")
    
    assert str(exc_info.value) == "Invalid API key"

def test_network_error():
    """Test NetworkError handling."""
    with pytest.raises(NetworkError) as exc_info:
        raise NetworkError("Connection timeout", status_code=408)
    
    assert str(exc_info.value) == "Connection timeout"
    assert exc_info.value.status_code == 408

def test_validation_error():
    """Test ValidationError for input validation."""
    with pytest.raises(ValidationError) as exc_info:
        raise ValidationError("Invalid input parameters")
    
    assert str(exc_info.value) == "Invalid input parameters"

def test_exception_logging(caplog):
    """Test that exceptions are logged correctly."""
    caplog.set_level(logging.ERROR)
    
    try:
        raise CoinGeckoAPIError("Logging test", status_code=500)
    except CoinGeckoAPIError:
        pass
    
    assert "CoinGecko API Error: Logging test (Status Code: 500)" in caplog.text