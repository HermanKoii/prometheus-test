import os
import pytest
from src.config import CoinGeckoConfig

def test_default_configuration():
    """Test default configuration without environment variables."""
    config = CoinGeckoConfig(env_file=None)
    
    # Default base URL should be set
    assert config.base_url == 'https://api.coingecko.com/api/v3'
    assert config.request_timeout == 10
    assert config.retries == 3
    assert config.api_key is None

def test_env_variable_configuration(monkeypatch):
    """Test configuration loaded from environment variables."""
    monkeypatch.setenv('COINGECKO_API_KEY', 'test_api_key')
    monkeypatch.setenv('COINGECKO_BASE_URL', 'https://custom-api.coingecko.com')
    monkeypatch.setenv('COINGECKO_REQUEST_TIMEOUT', '30')
    monkeypatch.setenv('COINGECKO_RETRIES', '5')
    
    config = CoinGeckoConfig(env_file=None)
    
    assert config.api_key == 'test_api_key'
    assert config.base_url == 'https://custom-api.coingecko.com'
    assert config.request_timeout == 30
    assert config.retries == 5

def test_constructor_priority():
    """Test that constructor arguments take priority over environment variables."""
    config = CoinGeckoConfig(
        api_key='constructor_key', 
        base_url='https://manual-url.com', 
        env_file=None
    )
    
    assert config.api_key == 'constructor_key'
    assert config.base_url == 'https://manual-url.com'

def test_configuration_to_dict():
    """Test converting configuration to dictionary."""
    config = CoinGeckoConfig(
        api_key='test_key', 
        base_url='https://test-url.com', 
        env_file=None
    )
    
    config_dict = config.to_dict()
    
    assert isinstance(config_dict, dict)
    assert config_dict['api_key'] == 'test_key'
    assert config_dict['base_url'] == 'https://test-url.com'
    assert config_dict['request_timeout'] == 10
    assert config_dict['retries'] == 3

def test_configuration_validation():
    """Test configuration validation."""
    with pytest.raises(ValueError, match='base URL is required'):
        # Forcing empty base URL should raise an error
        CoinGeckoConfig(base_url='   ', env_file=None)
    
    with pytest.raises(ValueError, match='base URL is required'):
        # Forcing empty base URL should raise an error
        CoinGeckoConfig(base_url='', env_file=None)