import os
import sys
import pytest

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.config import CoinGeckoConfig, ConfigurationError

def test_default_configuration():
    """Test default configuration initialization."""
    config = CoinGeckoConfig(base_url='https://api.coingecko.com/api/v3')
    assert config.base_url == 'https://api.coingecko.com/api/v3'
    assert config.api_key is None

def test_env_variable_configuration(monkeypatch):
    """Test configuration loading from environment variables."""
    monkeypatch.setenv('COINGECKO_BASE_URL', 'https://custom-api.coingecko.com')
    monkeypatch.setenv('COINGECKO_API_KEY', 'test_api_key')
    
    config = CoinGeckoConfig(base_url='https://custom-api.coingecko.com')
    assert config.base_url == 'https://custom-api.coingecko.com'
    assert config.api_key == 'test_api_key'

def test_constructor_priority(monkeypatch):
    """Test programmatic configuration overriding environment variables."""
    monkeypatch.setenv('COINGECKO_BASE_URL', 'https://env-api.coingecko.com')
    
    config = CoinGeckoConfig(
        base_url='https://programmatic-api.coingecko.com',
        api_key='programmatic_key'
    )
    
    assert config.base_url == 'https://programmatic-api.coingecko.com'
    assert config.api_key == 'programmatic_key'

def test_configuration_to_dict():
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

def test_configuration_validation():
    """Test configuration validation."""
    with pytest.raises(ValueError, match='base URL is required'):
        CoinGeckoConfig()