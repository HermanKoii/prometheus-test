import os
import pytest
from src.config import CoinGeckoConfig, ConfigurationError

def test_default_configuration():
    config = CoinGeckoConfig()
    assert config['api_base_url'] == 'https://api.coingecko.com/api/v3'
    assert config['api_timeout'] == 10
    assert config['max_retries'] == 3
    assert config['cache_duration'] == 300

def test_environment_variable_override(monkeypatch):
    monkeypatch.setenv('COINGECKO_API_BASE_URL', 'https://custom-api.com')
    monkeypatch.setenv('COINGECKO_API_TIMEOUT', '15')
    
    config = CoinGeckoConfig()
    assert config['api_base_url'] == 'https://custom-api.com'
    assert config['api_timeout'] == 15

def test_invalid_type_conversion(monkeypatch):
    monkeypatch.setenv('COINGECKO_API_TIMEOUT', 'invalid')
    
    with pytest.raises(ConfigurationError):
        CoinGeckoConfig()

def test_dictionary_and_get_method():
    config = CoinGeckoConfig()
    
    # Test dictionary-like access
    assert config['api_base_url'] == 'https://api.coingecko.com/api/v3'
    
    # Test get method with default
    assert config.get('non_existent_key', 'default') == 'default'
    
    # Test get method without default
    assert config.get('api_timeout') == 10

def test_missing_key():
    config = CoinGeckoConfig()
    
    with pytest.raises(KeyError):
        _ = config['non_existent_key']