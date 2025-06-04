import os
import pytest
from src.config import CoinGeckoConfig, ConfigurationError

def test_config_default_initialization():
    """Test default configuration initialization."""
    config = CoinGeckoConfig()
    assert config.base_url == 'https://api.coingecko.com/api/v3'
    assert config.api_key is None

def test_config_env_variables(monkeypatch):
    """Test configuration loading from environment variables."""
    monkeypatch.setenv('COINGECKO_BASE_URL', 'https://custom-api.coingecko.com')
    monkeypatch.setenv('COINGECKO_API_KEY', 'test_api_key')
    
    config = CoinGeckoConfig()
    assert config.base_url == 'https://custom-api.coingecko.com'
    assert config.api_key == 'test_api_key'

def test_config_programmatic_override(monkeypatch):
    """Test programmatic configuration overriding environment variables."""
    monkeypatch.setenv('COINGECKO_BASE_URL', 'https://env-api.coingecko.com')
    
    config = CoinGeckoConfig(
        base_url='https://programmatic-api.coingecko.com',
        api_key='programmatic_key'
    )
    
    assert config.base_url == 'https://programmatic-api.coingecko.com'
    assert config.api_key == 'programmatic_key'

def test_config_get_config():
    """Test get_config method returns correct dictionary."""
    config = CoinGeckoConfig(
        base_url='https://test-api.coingecko.com',
        api_key='test_key'
    )
    config_dict = config.get_config()
    
    assert config_dict == {
        'base_url': 'https://test-api.coingecko.com',
        'api_key': 'test_key'
    }

def test_invalid_base_url():
    """Test invalid base URL raises configuration error."""
    # Invalid protocol
    with pytest.raises(ConfigurationError, match="Base URL must start with http:// or https://"):
        CoinGeckoConfig(base_url='invalid_url')
    
    # Empty string
    with pytest.raises(ConfigurationError, match="Base URL must be a non-empty string"):
        CoinGeckoConfig(base_url='')
    
    # None input
    with pytest.raises(ConfigurationError, match="Base URL must be a non-empty string"):
        CoinGeckoConfig(base_url=None)
    
    # Non-string input
    with pytest.raises(ConfigurationError, match="Base URL must be a non-empty string"):
        CoinGeckoConfig(base_url=123)  # Non-string base URL