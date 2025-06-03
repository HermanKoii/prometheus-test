import os
import pytest
from src.config import CoinGeckoConfig

def test_default_configuration():
    """Test default configuration initialization."""
    config = CoinGeckoConfig()
    assert config.base_url == 'https://api.coingecko.com/api/v3'
    assert config.timeout == 10
    assert config.retries == 3

def test_custom_configuration():
    """Test custom configuration initialization."""
    config = CoinGeckoConfig(
        api_key='test_key', 
        base_url='https://custom.coingecko.com', 
        timeout=15, 
        retries=5
    )
    assert config.api_key == 'test_key'
    assert config.base_url == 'https://custom.coingecko.com'
    assert config.timeout == 15
    assert config.retries == 5

def test_env_configuration(monkeypatch):
    """Test configuration using environment variables."""
    monkeypatch.setenv('COINGECKO_API_KEY', 'env_test_key')
    monkeypatch.setenv('COINGECKO_BASE_URL', 'https://env.coingecko.com')
    
    config = CoinGeckoConfig()
    assert config.api_key == 'env_test_key'
    assert config.base_url == 'https://env.coingecko.com'

def test_invalid_base_url():
    """Test invalid base URL configuration."""
    with pytest.raises(ValueError, match="Base URL must start with http:// or https://"):
        CoinGeckoConfig(base_url='invalid_url')

def test_get_api_credentials():
    """Test get_api_credentials method."""
    config = CoinGeckoConfig(api_key='test_key', timeout=20)
    credentials = config.get_api_credentials()
    
    assert credentials['api_key'] == 'test_key'
    assert credentials['base_url'] == 'https://api.coingecko.com/api/v3'
    assert credentials['timeout'] == 20

def test_is_valid():
    """Test is_valid method for configuration."""
    valid_config = CoinGeckoConfig()
    assert valid_config.is_valid() is True
    
    with pytest.raises(ValueError):
        CoinGeckoConfig(base_url='invalid')  # This should fail validation