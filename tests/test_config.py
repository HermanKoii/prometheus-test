import os
import pytest
import json
from src.config import CoinGeckoConfig, ConfigurationError

def test_default_configuration():
    """Test default configuration parameters."""
    config = CoinGeckoConfig()
    assert config.get('base_url') == 'https://api.coingecko.com/api/v3'
    assert config.get('timeout') == 30
    assert config.get('api_key') is None

def test_explicit_configuration():
    """Test configuration with explicit parameters."""
    config = CoinGeckoConfig(
        api_key='test_key', 
        base_url='https://custom.api.com', 
        timeout=60
    )
    assert config.get('api_key') == 'test_key'
    assert config.get('base_url') == 'https://custom.api.com'
    assert config.get('timeout') == 60

def test_environment_variable_configuration(monkeypatch):
    """Test configuration from environment variables."""
    monkeypatch.setenv('COINGECKO_API_KEY', 'env_api_key')
    monkeypatch.setenv('COINGECKO_BASE_URL', 'https://env.api.com')
    monkeypatch.setenv('COINGECKO_TIMEOUT', '45')
    
    config = CoinGeckoConfig()
    assert config.get('api_key') == 'env_api_key'
    assert config.get('base_url') == 'https://env.api.com'
    assert config.get('timeout') == 45

def test_configuration_file(tmp_path):
    """Test configuration from JSON file."""
    config_data = {
        'api_key': 'file_api_key',
        'base_url': 'https://file.api.com',
        'timeout': 50
    }
    config_file = tmp_path / 'config.json'
    
    with open(config_file, 'w') as f:
        json.dump(config_data, f)
    
    config = CoinGeckoConfig(config_file=str(config_file))
    assert config.get('api_key') == 'file_api_key'
    assert config.get('base_url') == 'https://file.api.com'
    assert config.get('timeout') == 50

def test_invalid_timeout_configuration():
    """Test handling of invalid timeout configuration."""
    with pytest.raises(ConfigurationError, match="Invalid timeout value"):
        CoinGeckoConfig(timeout=-10)

def test_missing_base_url_configuration():
    """Test handling of missing base URL."""
    with pytest.raises(ConfigurationError, match="Base URL is required"):
        CoinGeckoConfig(base_url=None)

def test_configuration_priority():
    """Test configuration parameter priority."""
    # Explicit parameter should override env and file
    os.environ['COINGECKO_API_KEY'] = 'env_key'
    
    config = CoinGeckoConfig(api_key='explicit_key')
    assert config.get('api_key') == 'explicit_key'

def test_dictionary_style_access():
    """Test dictionary-style configuration access."""
    config = CoinGeckoConfig(base_url='https://test.api.com')
    assert config['base_url'] == 'https://test.api.com'
    
    with pytest.raises(KeyError):
        _ = config['non_existent_key']