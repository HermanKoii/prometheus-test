import os
import pytest
from src.coingecko_config import CoinGeckoConfig

def test_default_configuration():
    """Test default configuration initialization."""
    config = CoinGeckoConfig()
    
    assert config.base_url == 'https://api.coingecko.com/api/v3'
    assert config.default_currency == 'usd'
    assert config.timeout == 10
    assert config.api_key is None

def test_custom_configuration():
    """Test custom configuration initialization."""
    custom_config = CoinGeckoConfig(
        api_key='test_api_key',
        base_url='https://custom-api.example.com',
        default_currency='eur',
        timeout=15
    )
    
    assert custom_config.api_key == 'test_api_key'
    assert custom_config.base_url == 'https://custom-api.example.com'
    assert custom_config.default_currency == 'eur'
    assert custom_config.timeout == 15

def test_environment_variable_configuration(monkeypatch):
    """Test configuration using environment variables."""
    monkeypatch.setenv('COINGECKO_API_KEY', 'env_api_key')
    monkeypatch.setenv('COINGECKO_BASE_URL', 'https://env-api.example.com')
    
    config = CoinGeckoConfig()
    
    assert config.api_key == 'env_api_key'
    assert config.base_url == 'https://env-api.example.com'

def test_configuration_get_config():
    """Test get_config method."""
    config = CoinGeckoConfig(
        api_key='test_key',
        base_url='https://test-api.example.com',
        default_currency='gbp',
        timeout=20
    )
    
    config_dict = config.get_config()
    
    assert config_dict == {
        'api_key': 'test_key',
        'base_url': 'https://test-api.example.com',
        'default_currency': 'gbp',
        'timeout': 20
    }

def test_configuration_validation():
    """Test configuration validation."""
    valid_config = CoinGeckoConfig()
    assert valid_config.validate() is True
    
    invalid_config = CoinGeckoConfig(base_url='', timeout=0)
    assert invalid_config.validate() is False